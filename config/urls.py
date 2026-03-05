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

    path("api/countries/", include("apps.countries.urls")),

    path("api/indicators/", include("apps.indicators.urls")),

    path("api/portafolios/", include("apps.portfolios.urls")),

    path("api/riesgo/", include("apps.risk.urls")),
]