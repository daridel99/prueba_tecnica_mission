from django.contrib import admin
from .models import Pais


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("codigo_iso", "nombre", "region", "moneda_codigo", "activo")
    list_filter = ("region", "activo")
    search_fields = ("nombre", "codigo_iso", "moneda_codigo")