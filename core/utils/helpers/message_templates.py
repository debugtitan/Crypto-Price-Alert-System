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
    def alert_coin_price_trigger_success(target_price, current_price, direction):
        arrow_emoji = "⬆️" if direction == "HIGH" else "⬇️"
        message = f"""
            <div style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px; border-radius: 10px;">
                <h2 style="color: #2c3e50;">🚨 Price Alert Triggered! {arrow_emoji}</h2>
                <p style="color: #34495e; font-size: 16px;">
                    Your price alert for the coin has been triggered.
                </p>
                <p style="color: #2c3e50; font-size: 18px;">
                    Target Price: <strong>${target_price}</strong><br>
                    Current Price: <strong>${current_price}</strong><br>
                    Direction: <strong>{direction.capitalize()}</strong>
                </p>
                <p style="color: #34495e; font-size: 16px;">
                    Please check your portfolio for more details.
                </p>
            </div>
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
