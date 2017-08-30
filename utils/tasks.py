from celery.utils.log import get_task_logger
from django.conf import settings
from dynamicweb.celery import app
from django.core.mail import EmailMessage

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
