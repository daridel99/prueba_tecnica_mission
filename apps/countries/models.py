from django.db import models


class Pais(models.Model):

    class Region(models.TextChoices):
        ANDINA = "ANDINA"
        CONO_SUR = "CONO_SUR"
        CENTROAMERICA = "CENTROAMERICA"
        CARIBE = "CARIBE"

    codigo_iso = models.CharField(primary_key=True, max_length=3)
    nombre = models.CharField(max_length=100)
    moneda_codigo = models.CharField(max_length=10)
    moneda_nombre = models.CharField(max_length=50)
    region = models.CharField(max_length=20, choices=Region.choices)
    latitud = models.FloatField()
    longitud = models.FloatField()
    poblacion = models.BigIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["nombre"]
        
    def __str__(self):
        return self.nombre