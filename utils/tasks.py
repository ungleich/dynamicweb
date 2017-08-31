import tempfile

import cdist
import cdist.integration as cdist_integration
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
            cdist_instance_index = cdist_integration.instance_index
            cdist_index = next(cdist_instance_index)
            cdist_integration.configure_hosts_simple(hosts,
                                                     tmp_manifest.name,
                                                     index=cdist_index,
                                                     verbose=cdist.argparse.VERBOSE_TRACE)
            cdist_instance_index.free(cdist_index)
        except Exception as cdist_exception:
            logger.error(cdist_exception)
            return_value = False
    return return_value
