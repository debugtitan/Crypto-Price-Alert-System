from rest_framework import serializers
from core.v1.alerts.models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["id", "target_price", "triggered", "owner", "direction"]
        read_only_fields = ["triggered", "owner"]
