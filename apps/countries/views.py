from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Pais
from .serializers import PaisSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.indicators.models import IndicadorEconomico
from apps.indicators.serializers import IndicadorEconomicoSerializer
from apps.exchange.models import TipoCambio
from apps.exchange.serializers import TipoCambioSerializer
from django.core.management import call_command
from rest_framework.permissions import IsAdminUser

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "codigo_iso"

    @action(detail=True, methods=["get"])
    def indicadores(self, request, codigo_iso=None):
        pais = self.get_object()
        indicadores = IndicadorEconomico.objects.filter(pais=pais)

        serializer = IndicadorEconomicoSerializer(indicadores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path="tipo-cambio")
    def tipo_cambio(self, request, codigo_iso=None):
        pais = self.get_object()
        tipocambio = TipoCambio.objects.filter(pais=pais)

        serializer = TipoCambioSerializer(tipocambio, many=True)
        return Response(serializer.data)
    
    @action( detail=False, methods=["post"], url_path="sync-indicadores", permission_classes=[IsAdminUser])
    def sync_indicadores(self, request):

        call_command("sync_paises")
        call_command("sync_indicadores")

        return Response({
            "mensaje": "Sincronización de indicadores Finalizados"
        })