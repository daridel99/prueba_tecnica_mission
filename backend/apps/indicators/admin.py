from django.contrib import admin
from .models import IndicadorEconomico


@admin.register(IndicadorEconomico)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = ("pais", "tipo", "anio", "valor")
    list_filter = ("tipo", "anio", "fuente")
    search_fields = ("pais__nombre", "pais__codigo_iso")