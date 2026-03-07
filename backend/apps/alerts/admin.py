from django.contrib import admin
from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "pais", "severidad", "leida", "fecha_creacion")
    list_filter = ("severidad", "leida")