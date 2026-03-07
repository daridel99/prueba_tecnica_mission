from rest_framework.routers import DefaultRouter
from .views import IndicadorViewSet

router = DefaultRouter()
router.register(r"indicadores", IndicadorViewSet, basename="indicadores")

urlpatterns = router.urls