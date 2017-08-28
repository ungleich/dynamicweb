from dynamicweb.celery import app
from celery.utils.log import get_task_logger
from django.conf import settings
from cdist.integration import configure_hosts_simple
import cdist
import tempfile
import pathlib

logger = get_task_logger(__name__)


@app.task(bind=True, max_retries=settings.CELERY_MAX_RETRIES)
def save_ssh_key(hosts, keys):
    """
    Saves ssh key into the VMs of a user using cdist

    :param hosts: A list of hosts to be configured
    :param keys: A list of keys to be added
    """
    # Generate manifest to be used for configuring the hosts
    with tempfile.NamedTemporaryFile() as tmp_manifest:
        tmp_manifest.writelines(['__ssh_authorized_keys root \\',
                                 '  --key "{keys}"'.format(
                                     keys='\n'.join(keys))])

        f = pathlib.Path(tmp_manifest.name)
        configure_hosts_simple(hosts,
                               tmp_manifest.name,
                               verbose=cdist.argparse.VERBOSE_TRACE)


