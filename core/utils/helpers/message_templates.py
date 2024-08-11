from django.conf import settings

from core.utils.helpers.datetime import DateTime


class MessageTemplates:

    @staticmethod
    def email_verification_success():
        message = f"""
                <p style="color: #fff">Your email has been verified successfully.</p>
                """
        return message

    @staticmethod
    def email_login_email(token: str):

        message = f"""
                    <p style="color: #fff">Kindly login to your account with the below code.</p>
                    <h1 style="color: #fff">{token}</h1>
                    <p style="color: #fff"><b>The above code will expire in {DateTime.convert_seconds_to_hr_min(settings.EMAIL_LOGIN_TOKEN_EXPIRATION_SECS)}.</b></p>
                    """
        return message
