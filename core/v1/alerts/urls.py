from core.utils.helpers import routers
from . import views

router = routers.OptionalSlashRouter()

app_name = "alerts"
router.register(r"alerts", views.AlertViewSet, basename="alerts")
urlpatterns = router.urls
