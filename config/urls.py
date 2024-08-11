"""
URL configuration for crypto_alert_system project.
"""

from django.conf import settings
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Alerto API Documentation",
        default_version="v1",
        description="API Documentation for Alerto backend",
        terms_of_service="",
        contact=openapi.Contact(email="alts.devs@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path(f"api/v{settings.API_VERSION}/auth/", include("core.v1.users.urls")),
    path(f"api/v{settings.API_VERSION}/", include("core.v1.alerts.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
