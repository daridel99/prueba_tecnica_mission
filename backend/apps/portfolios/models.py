from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from apps.countries.models import Pais


class Portafolio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500, blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portafolios"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    es_publico = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "nombre"],
                name="unique_portafolio_usuario_nombre"
            )
        ]
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.nombre} - {self.usuario.email}"


class Posicion(models.Model):

    class TipoActivo(models.TextChoices):
        RENTA_FIJA = "RENTA_FIJA"
        RENTA_VARIABLE = "RENTA_VARIABLE"
        COMMODITIES = "COMMODITIES"
        MONEDA = "MONEDA"

    portafolio = models.ForeignKey(
        Portafolio,
        on_delete=models.CASCADE,
        related_name="posiciones"
    )
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    tipo_activo = models.CharField(max_length=20, choices=TipoActivo.choices)
    monto_inversion_usd = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField(null=True, blank=True)
    notas = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(fecha_salida__isnull=True) | Q(fecha_salida__gt=F("fecha_entrada")),
                name="fecha_salida_mayor_entrada"
            )
        ]

    def __str__(self):
        return f"{self.portafolio.nombre} - {self.pais.nombre}"