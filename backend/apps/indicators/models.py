from django.db import models


class IndicadorEconomico(models.Model):

    class TipoIndicador(models.TextChoices):
        PIB = "PIB", "Producto Interno Bruto"
        INFLACION = "INFLACION", "Inflación"
        DESEMPLEO = "DESEMPLEO", "Desempleo"
        BALANZA_COMERCIAL = "BALANZA_COMERCIAL", "Balanza Comercial"
        DEUDA_PIB = "DEUDA_PIB", "Deuda PIB"
        PIB_PERCAPITA = "PIB_PERCAPITA", "PIB Percapita"

    class Unidad(models.TextChoices):
        PORCENTAJE = "PORCENTAJE", "Porcentaje"
        USD = "USD", "USD"
        USD_MILES_MILLONES = "USD_MILES_MILLONES", "USD Miles de Millones"
    
    class Fuente(models.TextChoices):
        WORLD_BANK = "WORLD_BANK", "World Bank"
        MANUAL = "MANUAL", "Manual"

    pais = models.ForeignKey(
        "countries.Pais",
        on_delete=models.CASCADE,
        related_name="indicadores"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoIndicador.choices
    )

    unidad = models.CharField(
        max_length=20,
        choices=Unidad.choices
    )

    anio = models.IntegerField()

    valor = models.DecimalField(
        max_digits=20, 
        decimal_places=4
    )
    
    fuente = models.CharField(
        max_length=20,
        choices=Fuente.choices
    )

    fecha_actualizacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pais", "tipo", "anio"],
                name="unique_indicador_pais_tipo_anio"
            )
        ]
        ordering = ["-anio"]

    def __str__(self):
        return f"{self.pais.codigo_iso} - {self.tipo} - {self.anio}"