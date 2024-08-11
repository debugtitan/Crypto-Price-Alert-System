from django.conf import settings
from rest_framework.permissions import BasePermission


class FreeToAll(BasePermission):
    """Allows access to all"""

    def has_permission(self, request, view):
        return True


class IsGuestUser(BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    message: str

    def has_permission(self, request, view):
        self.message = "You are already logged in"
        return not request.user.is_authenticated
