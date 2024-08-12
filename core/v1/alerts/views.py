from rest_framework.viewsets import ViewSet
from rest_framework import status, decorators, response

from core.v1.alerts.serializers import AlertSerializer
from core.v1.alerts.models import Alert
from core.utils.helpers import mixins

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AlertViewSet(mixins.CustomRequestDataValidationMixin, ViewSet):
    """"""

    queryset = Alert.objects
    serializer_class = AlertSerializer

    def get_required_fields(self):
        if self.action == "create":
            return ["target_price"]
        return []

    @swagger_auto_schema(responses={200: AlertSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """
        retrieves alerts belonging to an authenticated user and returns them as serialized data.

        """
        user_alerts = Alert.objects.filter(owner=request.user)
        serializer = self.serializer_class(user_alerts, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AlertSerializer,
        responses={
            201: AlertSerializer,
            400: openapi.Response(
                description="Invalid data",
                examples={
                    "application/json": {"target_price": ["This field is required."]}
                },
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return response.Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        responses={
            204: "No content",
            404: openapi.Response(
                description="Alert not found",
                examples={
                    "application/json": {
                        "statusCode": 404,
                        "message": "Alert not found",
                        "status": "",
                    }
                },
            ),
        }
    )
    def destroy(self, request, pk=None):
        try:
            alert = Alert.objects.get(pk=pk, owner=request.user)
            alert.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except Alert.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
