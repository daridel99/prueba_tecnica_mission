from django.core.management.base import BaseCommand
from apps.countries.models import Pais
from apps.risk.services.irpc_service import IRPCService


class Command(BaseCommand):
    help = "Recalcula el índice de riesgo para todos los países"

    def handle(self, *args, **kwargs):

        self.stdout.write("Calculando índices de riesgo...")

        total = 0

        for pais in Pais.objects.filter(activo=True):

            IRPCService.calcular_irpc(pais)

            total += 1

            self.stdout.write(f"✔ Riesgo calculado para {pais.nombre}")

        self.stdout.write(
            self.style.SUCCESS(f"{total} países procesados correctamente")
        )

    