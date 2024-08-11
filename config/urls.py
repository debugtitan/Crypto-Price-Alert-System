"""
URL configuration for crypto_alert_system project.
"""

from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path(f"api/v{settings.API_VERSION}/auth/", include("core.v1.users.urls")),
]
