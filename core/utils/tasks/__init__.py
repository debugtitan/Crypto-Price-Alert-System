from celery import shared_task
from core.utils.helpers.email_client import EmailClient


@shared_task(bind=True)
def send_email_to_address(self, email_address, subject, message, name=""):
    email_messaging_helper = EmailClient(
        email_address, subject=subject, message=message
    )
    email_messaging_helper.send_mail()
