from django.db import models
from django.conf import settings


class LogActividad(models.Model):

    class Accion(models.TextChoices):
        CREAR = "CREAR"
        EDITAR = "EDITAR"
        ELIMINAR = "ELIMINAR"
        CONSULTAR = "CONSULTAR"
        LOGIN = "LOGIN"
        EXPORT = "EXPORT"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=Accion.choices)
    entidad_afectada = models.CharField(max_length=100)
    entidad_id = models.CharField(max_length=50)
    detalle = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.usuario.email} - {self.accion}"