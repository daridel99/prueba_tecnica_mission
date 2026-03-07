from rest_framework.routers import DefaultRouter
from .views import RiesgoViewSet

router = DefaultRouter()
router.register(r"", RiesgoViewSet, basename="riesgo")

urlpatterns = router.urls