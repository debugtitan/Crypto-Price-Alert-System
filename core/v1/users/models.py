from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from core.utils import enums


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError("The email field must not be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str,
        account_type: str = enums.AccountType.SUPER_ADMINISTRATOR.value,
        **extra_fields,
    ):
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("is_staff", True)

        if (
            account_type != enums.AccountType.SUPER_ADMINISTRATOR.value
            or account_type not in enums.AccountType.values()
        ):
            raise ValueError("Invalid account type for a superuser")

        extra_fields.setdefault("account_type", account_type)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, enums.BaseModelMixin):
    """default user models for crypto token price tracker"""

    email = models.EmailField(_("email address"), unique=True)

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("whether this user should be treated as verified."),
    )

    account_type = models.CharField(
        _("user roles"),
        choices=enums.AccountType.values(),
        default=enums.AccountType.CLIENT.value,
        help_text=_("user account roles and some fdeatures they can handle"),
    )

    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @staticmethod
    def get_email_signup_code_cache_reference(code):
        return f"EMAIL_SIGNUP_CODE_{code}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class UserSession(enums.BaseModelMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh = models.CharField(max_length=255, unique=True, null=True, blank=True)
    access = models.CharField(max_length=255, unique=True, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"
