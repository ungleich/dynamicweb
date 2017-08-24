from dynamicweb.celery import app
from celery.utils.log import get_task_logger
from django.conf import settings
from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineSerializer
from hosting.models import HostingOrder, HostingBill
from utils.forms import UserBillingAddressForm
from datetime import datetime
from membership.models import StripeCustomer
from django.core.mail import EmailMessage
from utils.models import BillingAddress
from celery.exceptions import MaxRetriesExceededError

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
def create_vm_task(self, vm_template_id, user, specs, template,
                   stripe_customer_id, billing_address_data,
                   billing_address_id,
                   charge, cc_details):
    vm_id = None
    try:
        final_price = specs.get('price')
        billing_address = BillingAddress.objects.filter(
            id=billing_address_id).first()
        customer = StripeCustomer.objects.filter(id=stripe_customer_id).first()
        # Create OpenNebulaManager
        manager = OpenNebulaManager(email=settings.OPENNEBULA_USERNAME,
                                    password=settings.OPENNEBULA_PASSWORD)

        # Create a vm using oneadmin, also specify the name
        vm_id = manager.create_vm(
            template_id=vm_template_id,
            specs=specs,
            ssh_key=settings.ONEADMIN_USER_SSH_PUBLIC_KEY,
            vm_name="{email}-{template_name}-{date}".format(
                email=user.get('email'),
                template_name=template.get('name'),
                date=int(datetime.now().strftime("%s")))
        )

        if vm_id is None:
            raise Exception("Could not create VM")

        # Create a Hosting Order
        order = HostingOrder.create(
            price=final_price,
            vm_id=vm_id,
            customer=customer,
            billing_address=billing_address
        )

        # Create a Hosting Bill
        HostingBill.create(
            customer=customer, billing_address=billing_address)

        # Create Billing Address for User if he does not have one
        if not customer.user.billing_addresses.count():
            billing_address_data.update({
                'user': customer.user.id
            })
            billing_address_user_form = UserBillingAddressForm(
                billing_address_data)
            billing_address_user_form.is_valid()
            billing_address_user_form.save()

        # Associate an order with a stripe subscription
        charge_object = DictDotLookup(charge)
        order.set_subscription_id(charge_object, cc_details)

        # If the Stripe payment succeeds, set order status approved
        order.set_approved()

        vm = VirtualMachineSerializer(manager.get_vm(vm_id)).data

        context = {
            'name': user.get('name'),
            'email': user.get('email'),
            'cores': specs.get('cpu'),
            'memory': specs.get('memory'),
            'storage': specs.get('disk_size'),
            'price': specs.get('price'),
            'template': template.get('name'),
            'vm.name': vm['name'],
            'vm.id': vm['vm_id'],
            'order.id': order.id
        }
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
                'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
                'to': ['info@ungleich.ch'],
                'body': ',\n'.join(str(i) for i in self.request.args)
            }
            email = EmailMessage(**email_data)
            email.send()
            return

    return vm_id


class DictDotLookup(object):
    """
    Creates objects that behave much like a dictionaries, but allow nested
    key access using object '.' (dot) lookups.
    """

    def __init__(self, d):
        for k in d:
            if isinstance(d[k], dict):
                self.__dict__[k] = DictDotLookup(d[k])
            elif isinstance(d[k], (list, tuple)):
                l = []
                for v in d[k]:
                    if isinstance(v, dict):
                        l.append(DictDotLookup(v))
                    else:
                        l.append(v)
                self.__dict__[k] = l
            else:
                self.__dict__[k] = d[k]

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

    def __iter__(self):
        return iter(self.__dict__.keys())
