from django.db import models
from apps.countries.models import Pais


class TipoCambio(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE) # pais.moneda_codigo -> moneda_origen
    moneda_destino = models.CharField(max_length=10, default="USD")
    tasa = models.DecimalField(max_digits=12, decimal_places=6)
    fecha = models.DateField()
    variacion_porcentual = models.DecimalField( max_digits=6, decimal_places=3, null=True, blank=True)
    fuente = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pais", "moneda_destino", "fecha"],
                name="unique_tipo_cambio_pais_fecha"
            )
        ]
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.pais.codigo_iso} -> {self.moneda_destino} ({self.fecha})"