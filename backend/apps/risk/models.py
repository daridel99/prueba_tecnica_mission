from django.db import models
from django.db.models import Q
from apps.countries.models import Pais


class IndiceRiesgo(models.Model):

    class NivelRiesgo(models.TextChoices):
        BAJO = "BAJO"
        MODERADO = "MODERADO"
        ALTO = "ALTO"
        CRITICO = "CRITICO"

    pais = models.ForeignKey(
        Pais,
        on_delete=models.CASCADE,
        related_name="indices_riesgo")

    fecha_calculo = models.DateField()

    score_economico = models.FloatField()
    score_cambiario = models.FloatField()
    score_estabilidad = models.FloatField()
    indice_compuesto = models.FloatField()

    nivel_riesgo = models.CharField(
        max_length=20,
        choices=NivelRiesgo.choices)

    detalle_calculo = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pais", "fecha_calculo"],
                name="unique_riesgo_pais_fecha"
            ),
            models.CheckConstraint(
                condition=Q(indice_compuesto__gte=0) & Q(indice_compuesto__lte=100),
                name="indice_compuesto_entre_0_100"
            ),
            models.CheckConstraint(
                condition=Q(score_economico__gte=0) & Q(score_economico__lte=100),
                name="score_economico_entre_0_100"
            ),
            models.CheckConstraint(
                condition=Q(score_cambiario__gte=0) & Q(score_cambiario__lte=100),
                name="score_cambiario_entre_0_100"
            ),
            models.CheckConstraint(
                condition=Q(score_estabilidad__gte=0) & Q(score_estabilidad__lte=100),
                name="score_estabilidad_entre_0_100"
            )
        ]

        ordering = ["-fecha_calculo"]

        indexes = [
            models.Index(fields=["pais"]),
            models.Index(fields=["-fecha_calculo"]),
        ]

    def __str__(self):
        return f"{self.pais.codigo_iso} - {self.indice_compuesto} ({self.nivel_riesgo})"
