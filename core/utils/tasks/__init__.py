from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import PeriodicTask
from core.utils.helpers.blockchain import price_sol
from core.utils.helpers.email_client import EmailClient
from core.utils.helpers.message_templates import MessageTemplates
from core.v1.alerts.models import Alert


@shared_task
def clear_out_periodic_tasks():
    try:
        PeriodicTask.objects.filter(expires__lte=timezone.now()).delete()
    except Exception as e:
        pass


@shared_task(bind=True)
def send_email_to_address(self, email_address, subject, message, name=""):
    email_messaging_helper = EmailClient(
        email_address, subject=subject, message=message
    )
    email_messaging_helper.send_mail()


@shared_task
def price_fetcher():
    current_price = price_sol()
    print(current_price)
    alerts = Alert.objects.filter(triggered=False)
    for alert in alerts:

        if (alert.direction == "HIGH" and current_price >= alert.target_price) or (
            alert.direction == "LOW" and current_price <= alert.target_price
        ):
            message = MessageTemplates.alert_coin_price_trigger_success(
                alert.target_price, current_price, alert.direction
            )

            email_messaging_helper = EmailClient(
                alert.owner.email, subject="Price Trigger", message=message
            )
            email_messaging_helper.send_mail()

            alert.triggered = True
            alert.save()
