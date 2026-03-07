from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("api/auth/", include("apps.users.urls")),

    path("api/", include("apps.countries.urls")),

    path("api/dashboard/", include("apps.dashboard.urls")),

    path("api/indicators/", include("apps.indicators.urls")),

    path("api/portafolios/", include("apps.portfolios.urls")),

    path("api/alertas/", include("apps.alerts.urls")),

    path("api/riesgo/", include("apps.risk.urls")),
]
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]