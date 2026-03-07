from django.contrib import admin
from .models import IndiceRiesgo


@admin.register(IndiceRiesgo)
class IndiceRiesgoAdmin(admin.ModelAdmin):
    list_display = ("pais", "indice_compuesto", "nivel_riesgo", "fecha_calculo")
    list_filter = ("nivel_riesgo",)