from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.core.management import call_command
from django.shortcuts import get_object_or_404

from django.db.models import OuterRef, Subquery
from apps.countries.models import Pais
from apps.risk.models import IndiceRiesgo
from .services.irpc_service import IRPCService


class RiesgoViewSet(viewsets.ViewSet):

    def list(self, request):
        latest = IndiceRiesgo.objects.filter(
            pais=OuterRef("pais")
        ).order_by("-fecha_calculo")
        riesgos = IndiceRiesgo.objects.filter(
            pk__in=Subquery(latest.values("pk")[:1])
        ).select_related("pais").order_by("-indice_compuesto")
        data = [{
            "pais": r.pais.nombre,
            "codigo_iso": r.pais.codigo_iso,
            "indice": r.indice_compuesto,
            "nivel": r.nivel_riesgo,
            "fecha": r.fecha_calculo.isoformat()
        } for r in riesgos]
        return Response(data)

    def retrieve(self, request, pk=None):
        pais = get_object_or_404(Pais, codigo_iso=pk)
        indice = IndiceRiesgo.objects.filter(pais=pais).order_by("-fecha_calculo").first()
        if not indice:
            return Response({"detail": "No hay indice de riesgo calculado para este pais."}, status=404)
        return Response({
            "pais": pais.nombre, "codigo_iso": pais.codigo_iso,
            "indice": indice.indice_compuesto, "nivel": indice.nivel_riesgo,
            "score_economico": indice.score_economico,
            "score_cambiario": indice.score_cambiario,
            "score_estabilidad": indice.score_estabilidad,
            "fecha": indice.fecha_calculo.isoformat(),
            "detalle": indice.detalle_calculo
        })

    @action(detail=True, methods=["get"])
    def historico(self, request, pk=None):
        historico = IndiceRiesgo.objects.filter(pais__codigo_iso=pk).select_related("pais").order_by("-fecha_calculo")[:100]
        data = [{
            "pais": h.pais.codigo_iso, "fecha": h.fecha_calculo.isoformat(),
            "indice": h.indice_compuesto, "nivel": h.nivel_riesgo
        } for h in historico]
        return Response(data)

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def calcular(self, request):
        call_command("recalcular_riesgo")
        return Response({"mensaje": "Recalculo de riesgo ejecutado correctamente"})
