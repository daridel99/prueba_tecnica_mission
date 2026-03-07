from django.contrib import admin
from .models import LogActividad


@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ("usuario", "accion", "entidad_afectada", "fecha")
    list_filter = ("accion",)