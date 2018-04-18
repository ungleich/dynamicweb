from datetime import datetime

from celery.exceptions import MaxRetriesExceededError
from celery.utils.log import get_task_logger
from celery import current_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from dynamicweb.celery import app
from hosting.models import HostingOrder
from membership.models import CustomUser
from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineSerializer
from utils.hosting_utils import get_all_public_keys, get_or_create_vm_detail
from utils.mailer import BaseEmail
from utils.stripe_utils import StripeUtils

logger = get_task_logger(__name__)


def retry_task(task, exception=None):
    """Retries the specified task using a "backing off countdown",
    meaning that the interval between retries grows exponentially
    with every retry.

    Arguments:
        task:
            The task to retry.

        exception:
            Optionally, the exception that caused the retry.
    """

    def backoff(attempts):
        return 2 ** attempts

    kwargs = {
        'countdown': backoff(task.request.retries),
    }

    if exception:
        kwargs['exc'] = exception

    raise task.retry(**kwargs)


@app.task(bind=True, max_retries=settings.CELERY_MAX_RETRIES)
def create_vm_task(self, vm_template_id, user, specs, template, order_id):
    logger.debug(
        "Running create_vm_task on {}".format(current_task.request.hostname))
    vm_id = None
    try:
        if 'pass' in user:
            on_user = user.get('email')
            on_pass = user.get('pass')
            logger.debug("Using user {user} to create VM".format(user=on_user))
            vm_name = None
        else:
            on_user = settings.OPENNEBULA_USERNAME
            on_pass = settings.OPENNEBULA_PASSWORD
            logger.debug("Using OpenNebula admin user to create VM")
            vm_name = "{email}-{template_name}-{date}".format(
                email=user.get('email'),
                template_name=template.get('name'),
                date=int(datetime.now().strftime("%s")))

        # Create OpenNebulaManager
        manager = OpenNebulaManager(email=on_user, password=on_pass)

        vm_id = manager.create_vm(
            template_id=vm_template_id,
            specs=specs,
            ssh_key=settings.ONEADMIN_USER_SSH_PUBLIC_KEY,
            vm_name=vm_name
        )

        if vm_id is None:
            raise Exception("Could not create VM")

        # Update HostingOrder with the created vm_id
        hosting_order = HostingOrder.objects.filter(id=order_id).first()
        error_msg = None
        if hosting_order:
            logger.debug(
                "Updating hosting_order {} with vm_id={}".format(
                    hosting_order.id, vm_id
                )
            )
            hosting_order.vm_id = vm_id
            hosting_order.save()
        else:
            error_msg = (
                "HostingOrder with id {order_id} not found. This means that "
                "the hosting order was not created and/or it is/was not "
                "associated with VM with id {vm_id}".format(
                    order_id=order_id, vm_id=vm_id
                )
            )
            logger.error(error_msg)

        stripe_utils = StripeUtils()
        result = stripe_utils.set_subscription_metadata(
            subscription_id=hosting_order.subscription_id,
            metadata={"VM_ID": str(vm_id)}
        )

        if result.get('error') is not None:
            emsg = "Could not update subscription metadata for {sub}".format(
                    sub=hosting_order.subscription_id
                )
            logger.error(emsg)
            if error_msg:
                error_msg += emsg
            else:
                error_msg = emsg

        vm = VirtualMachineSerializer(manager.get_vm(vm_id)).data

        context = {
            'name': user.get('name'),
            'email': user.get('email'),
            'cores': specs.get('cpu'),
            'memory': specs.get('memory'),
            'storage': specs.get('disk_size'),
            'price': specs.get('price'),
            'template': template.get('name'),
            'vm_name': vm.get('name'),
            'vm_id': vm['vm_id'],
            'order_id': order_id
        }

        if error_msg:
            context['errors'] = error_msg
        email_data = {
            'subject': settings.DCL_TEXT + " Order from %s" % context['email'],
            'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
            'to': ['info@ungleich.ch'],
            'body': "\n".join(
                ["%s=%s" % (k, v) for (k, v) in context.items()]),
            'reply_to': [context['email']],
        }
        email = EmailMessage(**email_data)
        email.send()

        if 'pass' in user:
            lang = 'en-us'
            if user.get('language') is not None:
                logger.debug(
                    "Language is set to {}".format(user.get('language')))
                lang = user.get('language')
            translation.activate(lang)
            # Send notification to the user as soon as VM has been booked
            context = {
                'base_url': "{0}://{1}".format(user.get('request_scheme'),
                                               user.get('request_host')),
                'order_url': reverse('hosting:orders',
                                     kwargs={'pk': order_id}),
                'page_header': _(
                    'Your New VM %(vm_name)s at Data Center Light') % {
                    'vm_name': vm.get('name')},
                'vm_name': vm.get('name')
            }
            email_data = {
                'subject': context.get('page_header'),
                'to': user.get('email'),
                'context': context,
                'template_name': 'new_booked_vm',
                'template_path': 'hosting/emails/',
                'from_address': settings.DCL_SUPPORT_FROM_ADDRESS,
            }
            email = BaseEmail(**email_data)
            email.send()

            # try to see if we have the IP and that if the ssh keys can
            # be configured
            new_host = manager.get_primary_ipv4(vm_id)
            logger.debug("New VM ID is {vm_id}".format(vm_id=vm_id))
            if new_host is not None:
                custom_user = CustomUser.objects.get(email=user.get('email'))
                get_or_create_vm_detail(custom_user, manager, vm_id)
                if custom_user is not None:
                    public_keys = get_all_public_keys(custom_user)
                    keys = [{'value': key, 'state': True} for key in
                            public_keys]
                    if len(keys) > 0:
                        logger.debug(
                            "Calling configure on {host} for "
                            "{num_keys} keys".format(
                                host=new_host, num_keys=len(keys)))
                        # Let's delay the task by 75 seconds to be sure
                        # that we run the cdist configure after the host
                        # is up
                        manager.manage_public_key(keys,
                                                  hosts=[new_host],
                                                  countdown=75)
    except Exception as e:
        logger.error(str(e))
        try:
            retry_task(self)
        except MaxRetriesExceededError:
            msg_text = 'Finished {} retries for create_vm_task'.format(
                self.request.retries)
            logger.error(msg_text)
            # Try sending email and stop
            email_data = {
                'subject': '{} CELERY TASK ERROR: {}'.format(settings.DCL_TEXT,
                                                             msg_text),
                'from_email': current_task.request.hostname,
                'to': settings.DCL_ERROR_EMAILS_TO_LIST,
                'body': ',\n'.join(str(i) for i in self.request.args)
            }
            email = EmailMessage(**email_data)
            email.send()
            return

    return vm_id
