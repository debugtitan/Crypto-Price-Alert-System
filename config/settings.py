"""
Django settings for crypto_alert_system project.

"""

import os
from pathlib import Path
from celery.schedules import crontab
from django.utils.timezone import timedelta
from corsheaders.defaults import default_headers as cors_default_headers
from config.celery.queue import CeleryQueue
from . import env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", "*****")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", True)
PRODUCTION = env.bool("PRODUCTION", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOST", default=["*"])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_celery_beat",
    "drf_yasg",
]

PROJECT_APPS = [
    "core.v1.users.apps.UsersConfig",
    "core.utils.apps.UtilsConfig",
    "core.v1.alerts.apps.AlertsConfig",
]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database

if not PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env.str(
                "DJANGO_POSTGRESQL_ENGINE", "django.db.backends.postgresql_psycopg2"
            ),
            "NAME": env.str("DJANGO_POSTGRES_NAME", "***"),
            "USER": env.str("DJANGO_POSTGRES_USER", "***"),
            "PASSWORD": env.str("DJANGO_POSTGRES_PASSWORD", "***"),
            "HOST": env.str("DJANGO_POSTGRES_HOST", "*****"),
            "PORT": env.int("DJANGO_POSTGRES_PORT", 5432),
        },
    }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#   CORS
if not env.bool("DJANGO_CORS_ALLOW_ALL_ORIGINS", default=False):
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = env.list(
        "DJANGO_CORS_ALLOWED_ORIGINS",
        default=[],
    )
else:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(cors_default_headers) + [
    "secret-key",
]


#   DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"anon": "50/minute"},
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "EXCEPTION_HANDLER": "core.utils.exceptions.exceptions.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

#   User Model
AUTH_USER_MODEL = "users.User"

# Auth Backend
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Session Engine
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# ___________ API AND VERSIONING ____________
API_VERSION = env.str("API_VERSION", default="1")


EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS = env.int(
    "DJANGO_EMAIL_VERIFICATION_TOKEN_EXPIRATION_SECS", default=(60 * 10)
)

EMAIL_LOGIN_TOKEN_EXPIRATION_SECS = env.int(
    "DJANGO_EMAIL_LOGIN_TOKEN_EXPIRATION_SECS", default=(60 * 10)
)

DJANGO_EMAIL_LOGIN_MASTER_TOKEN = env.str(
    "DJANGO_EMAIL_LOGIN_MASTER_TOKEN", default=SECRET_KEY
)

# ______________________REDIS____________________________
REDIS_HOST = env.str("REDIS_HOST", default="localhost")
REDIS_PORT = env.int("REDIS_PORT", default=6379)

# ______________________ Cache _______________________________
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
    }
}

CACHE_TTL = env.int("VIEW_CACHE_TTL_SECS", 60 * 15)


# ___________________________________Celery_________________________________________
CELERY_BROKER = env.str("CELERY_BROKER")
CELERY_BROKER_URL = CELERY_BROKER
CELERY_RESULT_BACKEND = env.str("CELERY_BACKEND")
CELERY_TIMEZONE = env.str("CELERY_TIMEZONE", default="UTC")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_QUEUES = CeleryQueue.queues()


CELERY_BEAT_SCHEDULE = {
    "clear_out_expired_periodic_tasks": {
        "task": "core.utils.tasks.clear_out_periodic_tasks",
        "schedule": crontab(hour="*/2"),
        "options": {"queue": "beats"},
    },
    "price_trigger_checker": {
        "task": "core.utils.tasks.price_fetcher",
        "schedule": timedelta(seconds=8),
        "options": {"queue": "beats"},
    },
}


# ___________EMAIL______________________
EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="***")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", True)
EMAIL_USE_TSL = env.bool("EMAIL_USE_TSL", False)
EMAIL_HOST = env.str("EMAIL_HOST", default="***")
EMAIL_PORT = env.int("EMAIL_PORT", 465)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="***")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="***")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}
