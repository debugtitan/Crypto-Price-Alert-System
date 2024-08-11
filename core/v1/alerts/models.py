from django.db import models
from core.utils import enums


class Alert(enums.BaseModelMixin):
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="alerts",
    )
    
    
