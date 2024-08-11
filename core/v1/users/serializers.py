from rest_framework.serializers import ModelSerializer
from core.v1.users.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"