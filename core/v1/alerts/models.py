from django.db import models
from django.utils.translation import gettext_lazy as _
from core.utils import enums


class Alert(enums.BaseModelMixin):
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="alerts",
    )

    target_price = models.DecimalField(
        _("target price"), decimal_places=2, max_digits=15
    )

    direction = models.CharField(
        _("price direction"),
        choices=enums.DirectionType.choices(),
        default=enums.DirectionType.HIGH.value,
        max_length=5,
    )
    triggered = models.BooleanField(default=False, help_text="treat alert as triggered")

    def __str__(self):
        return f"{self.user} - {self.coin} - {self.target_price}"
