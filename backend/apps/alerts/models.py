from django.db import models
from django.conf import settings
from apps.countries.models import Pais


class Alerta(models.Model):

    class TipoAlerta(models.TextChoices):
        RIESGO = "RIESGO"
        TIPO_CAMBIO = "TIPO_CAMBIO"
        INDICADOR = "INDICADOR"

    class Severidad(models.TextChoices):
        INFO = "INFO"
        WARNING = "WARNING"
        CRITICAL = "CRITICAL"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    tipo_alerta = models.CharField(max_length=20, choices=TipoAlerta.choices)
    severidad = models.CharField(max_length=20, choices=Severidad.choices)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo