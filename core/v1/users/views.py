import re
from django.conf import settings
from django.core import validators as django_core_validators
from django.db import transaction
from rest_framework import viewsets, status, response, decorators
from rest_framework_simplejwt.tokens import RefreshToken
from config.celery.queue import CeleryQueue
from core.v1.users.models import UserSession, User
from core.v1.users import serializers
from core.utils.helpers import permissions, redis, security, message_templates
from core.utils.helpers.mixins import CustomRequestDataValidationMixin
from core.utils.exceptions import CustomException
from core.utils import tasks as global_background_tasks


class AuthViewSet(
    CustomRequestDataValidationMixin,
    viewsets.ViewSet,
):
    """Authentication viewsets for users"""

    queryset = User.objects
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return self.queryset.all()

    def get_required_fields(self):
        if self.action == "initialize_email_login":
            return ["email"]
        elif self.action == "finalize_email_login":
            return ["token", "email"]

        return []

    def get_permissions(self):
        if self.action in [
            "initialize_email_login",
            "finalize_email_login",
        ]:
            return [permissions.IsGuestUser()]

        elif self.action == "helper":
            return [permissions.IsGuestUser()]

        return super().get_permissions()

    @staticmethod
    def get_redirect_uri_from_redirect_uri_content(redirect_uri_content: str):
        pattern = re.compile(r"(.+)\?.+")
        match_pattern = pattern.match(redirect_uri_content)
        if match_pattern:
            return match_pattern.group(1)

    @decorators.action(detail=False, methods=["post"])
    def initialize_email_login(self, request, *args, **kwargs):
        email = request.data.get("email").strip()
        django_core_validators.validate_email(email)

        token = security.Token.create_otp()
        cache_instance = redis.RedisTools(
            User.get_email_signup_code_cache_reference(token),
            ttl=settings.EMAIL_LOGIN_TOKEN_EXPIRATION_SECS,
        )
        cache_instance.cache_value = {"email": email}
        message = message_templates.MessageTemplates.email_login_email(token)
        try:
            instance = User.objects.get(email=email)
            instance.send_mail("Login To Your Account", message)
        except User.DoesNotExist:
            global_background_tasks.send_email_to_address.apply_async(
                (email, "Login To Your Account", message),
                queue=CeleryQueue.Definitions.EMAIL_NOTIFICATION,
            )
        return response.Response(
            status=status.HTTP_200_OK,
            data={"message": f"A login code has been sent to {email}"},
        )

    @decorators.action(detail=False, methods=["post"])
    @transaction.atomic
    def finalize_email_login(self, request, *args, **kwargs):
        token = request.data.get("token")
        email = request.data.get("email")
        cache_instance = redis.RedisTools(
            User.get_email_signup_code_cache_reference(token),
            ttl=settings.EMAIL_LOGIN_TOKEN_EXPIRATION_SECS,
        )

        if str(token) != settings.DJANGO_EMAIL_LOGIN_MASTER_TOKEN:
            if not cache_instance.cache_value:
                raise CustomException(
                    message="You specified an invalid token",
                    errors=["invalid token"],
                )
            if cache_instance.cache_value.get("email") != email:
                raise CustomException(
                    message="You specified an invalid email",
                    errors=["invalid email"],
                )
        try:
            instance = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            instance = User.objects.create(email=email.lower())
            serializer = serializers.UserSerializer(
                instance=instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # Invalidate the cache only when successful
        cache_instance.cache_value = None
        (not instance.is_email_verified) and instance.verify_email()
        auth_token = instance.retrieve_auth_token()

        try:
            session = UserSession.objects.filter(user=instance).first()
            if session and session.is_active:
                try:
                    token = RefreshToken(session.refresh)
                    token.blacklist()
                except Exception as e:
                    pass
                session.delete()
        except UserSession.DoesNotExist:
            UserSession.objects.create(
                user=instance,
                refresh=auth_token["refresh"],
                access=auth_token["access"],
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
                is_active=True,
            )

        serializer = serializers.UserSerializer(instance=instance)
        response_data = {**serializer.data, "token": auth_token}
        return response.Response(
            status=status.HTTP_200_OK,
            data=response_data,
        )
