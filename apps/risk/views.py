from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.management import call_command

from apps.countries.models import Pais
from apps.risk.models import IndiceRiesgo
from .services.irpc_service import IRPCService


class RiesgoViewSet(viewsets.ViewSet):

    # GET /api/riesgo/
    def list(self, request):

        riesgos = (
            IndiceRiesgo.objects
            .select_related("pais")
            .order_by("-indice_compuesto")
        )

        data = []

        for r in riesgos:
            data.append({
                "pais": r.pais.nombre,
                "codigo_iso": r.pais.codigo_iso,
                "indice": r.indice_compuesto,
                "nivel": r.nivel_riesgo,
                "fecha": r.fecha_calculo.strftime("%d:%m:%YT%H:%M")
            })

        return Response(data)

    # GET /api/riesgo/{codigo_iso}/
    def retrieve(self, request, pk=None):

        pais = Pais.objects.get(codigo_iso=pk)

        indice = IRPCService.calcular_irpc(pais)

        return Response({
            "pais": pais.nombre,
            "codigo_iso": pais.codigo_iso,
            "indice": indice.indice_compuesto,
            "nivel": indice.nivel_riesgo
        })

    # GET /api/riesgo/{codigo_iso}/historico/
    @action(detail=True, methods=["get"])
    def historico(self, request, pk=None):

        historico = (
            IndiceRiesgo.objects
            .filter(pais__codigo_iso=pk)
            .order_by("-fecha_calculo")
        )

        data = []

        for h in historico:
            
            data.append({
                "pais": h.pais.codigo_iso,
                "fecha": h.fecha_calculo.strftime("%d:%m:%YT%H:%M"),
                "indice": h.indice_compuesto,
                "nivel": h.nivel_riesgo
            })

        return Response(data)

    # POST /api/riesgo/calcular/
    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def calcular(self, request):

        call_command("recalcular_riesgo")

        return Response({
            "mensaje": "Recalculo de riesgo ejecutado correctamente"
        })