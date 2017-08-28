import cdist
import tempfile
from cdist.integration import configure_hosts_simple
from celery.utils.log import get_task_logger
from django.conf import settings

from dynamicweb.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True, max_retries=settings.CELERY_MAX_RETRIES)
def save_ssh_key(self, hosts, keys):
    """
    Saves ssh key into the VMs of a user using cdist

    :param hosts: A list of hosts to be configured
    :param keys: A list of keys to be added
    """
    return_value = True
    with tempfile.NamedTemporaryFile() as tmp_manifest:
        # Generate manifest to be used for configuring the hosts
        tmp_manifest.writelines([b'__ssh_authorized_keys root \\',
                                 '  --key "{keys}"'.format(
                                     keys='\n'.join(keys)).encode('utf-8')])
        try:
            configure_hosts_simple(hosts,
                                   tmp_manifest.name,
                                   verbose=cdist.argparse.VERBOSE_TRACE)
        except Exception as cdist_exception:
            logger.error(cdist_exception)
            return_value = False
    return return_value
