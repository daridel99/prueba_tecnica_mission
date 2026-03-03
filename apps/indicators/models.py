from django.db import models


class IndicadorEconomico(models.Model):

    class TipoIndicador(models.TextChoices):
        PIB = "PIB", "Producto Interno Bruto"
        INFLACION = "INFLACION", "Inflación"
        DESEMPLEO = "DESEMPLEO", "Desempleo"

    pais = models.ForeignKey(
        "countries.Pais",
        on_delete=models.CASCADE,
        related_name="indicadores"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TipoIndicador.choices
    )

    anio = models.IntegerField()
    valor = models.FloatField()

    fuente = models.CharField(max_length=100)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("pais", "tipo", "anio")
        ordering = ["-anio"]

    def __str__(self):
        return f"{self.pais.codigo_iso} - {self.tipo} - {self.anio}"