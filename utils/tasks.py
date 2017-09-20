import tempfile

import cdist
from cdist.integration import configure_hosts_simple
from celery.result import AsyncResult
from celery import current_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMessage

from dynamicweb.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True, max_retries=settings.CELERY_MAX_RETRIES)
def send_plain_email_task(self, email_data):
    """
    This is a generic celery task to be used for sending emails.
    A celery wrapper task for EmailMessage

    :param self:
    :param email_data: A dict of all needed email headers
    :return:
    """
    email = EmailMessage(**email_data)
    email.send()


@app.task(bind=True, max_retries=settings.CELERY_MAX_RETRIES)
def save_ssh_key(self, hosts, keys):
    """
    Saves ssh key into the VMs of a user using cdist

    :param hosts: A list of hosts to be configured
    :param keys: A list of keys to be added. A key should be dict of the
           form    {
                       'value': 'sha-.....', # public key as string
                       'state': True         # whether key is to be added or
                    }                        # removed
    """
    logger.debug(
        "Running save_ssh_key on {}".format(current_task.request.hostname))
    logger.debug("""Running save_ssh_key task for
                    Hosts: {hosts_str}
                    Keys: {keys_str}""".format(hosts_str=", ".join(hosts),
                                               keys_str=", ".join([
                                                   "{value}->{state}".format(
                                                       value=key.get('value'),
                                                       state=str(
                                                           key.get('state')))
                                                   for key in keys]))
                 )
    return_value = True
    with tempfile.NamedTemporaryFile(delete=True) as tmp_manifest:
        # Generate manifest to be used for configuring the hosts
        lines_list = [
            '  --key "{key}" --state {state} \\\n'.format(
                key=key['value'],
                state='present' if key['state'] else 'absent'
            ).encode('utf-8')
            for key in keys]
        lines_list.insert(0, b'__ssh_authorized_keys root \\\n')
        tmp_manifest.writelines(lines_list)
        tmp_manifest.flush()
        try:
            configure_hosts_simple(hosts,
                                   tmp_manifest.name,
                                   verbose=cdist.argparse.VERBOSE_TRACE)
        except Exception as cdist_exception:
            logger.error(cdist_exception)
            return_value = False
            email_data = {
                'subject': "celery save_ssh_key error - task id {0}".format(
                    self.request.id.__str__()),
                'from_email': current_task.request.hostname,
                'to': settings.DCL_ERROR_EMAILS_TO_LIST,
                'body': "Task Id: {0}\nResult: {1}\nTraceback: {2}".format(
                    self.request.id.__str__(), False, str(cdist_exception)),
            }
            send_plain_email_task(email_data)
    return return_value


@app.task
def save_ssh_key_error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    logger.error('Task {0} raised exception: {1!r}\n{2!r}'.format(
        uuid, exc, result.traceback))
    email_data = {
        'subject': "[celery error] Save SSH key error {0}".format(uuid),
        'from_email': current_task.request.hostname,
        'to': settings.DCL_ERROR_EMAILS_TO_LIST,
        'body': "Task Id: {0}\nResult: {1}\nTraceback: {2}".format(
            uuid, exc, result.traceback),
    }
    send_plain_email_task(email_data)
