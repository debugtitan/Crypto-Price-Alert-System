from celery import shared_task
from django.contrib.auth import get_user_model


@shared_task
def send_email_to_address(user_id: int, subject, message):
    UserModel = get_user_model()
    instance = UserModel.objects.get(id=user_id)
    email_messaging_helper = email_messaging.EmailClient(
        instance.email, subject, message, instance.short_name
    )
    email_messaging_helper.send_mail()
