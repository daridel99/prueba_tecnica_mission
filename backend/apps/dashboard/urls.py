from django.urls import path
from .views import (
    DashboardResumen,
    DashboardMapa,
    DashboardTendencias
)

urlpatterns = [
    path("resumen/", DashboardResumen.as_view()),
    path("mapa/", DashboardMapa.as_view()),
    path("tendencias/", DashboardTendencias.as_view()),
]