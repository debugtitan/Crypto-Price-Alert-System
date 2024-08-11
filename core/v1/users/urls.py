from core.utils.helpers import routers
from . import views


router = routers.OptionalSlashRouter()

app_name = "user"
router.register("", views.AuthViewSet, basename="auth")
urlpatterns = router.urls
