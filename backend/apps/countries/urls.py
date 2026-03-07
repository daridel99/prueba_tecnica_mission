from rest_framework.routers import DefaultRouter
from .views import PaisViewSet

router = DefaultRouter()
router.register(r"paises", PaisViewSet, basename="paises")

urlpatterns = router.urls