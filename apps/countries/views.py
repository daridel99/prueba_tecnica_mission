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
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "codigo_iso"

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = [
            "region"
        ]

    search_fields = [
        "nombre",
        "codigo_iso",
        "moneda_codigo",
        "moneda_nombre"
    ]

    ordering_fields = [
        "nombre",
        "poblacion",
        "region"
    ]

    @action(detail=True, methods=["get"])
    def indicadores(self, request, codigo_iso=None):
        pais = self.get_object()
        indicadores = IndicadorEconomico.objects.filter(pais=pais)

        serializer = IndicadorEconomicoSerializer(indicadores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path="tipo-cambio")
    def tipo_cambio(self, request, codigo_iso=None):
        pais = self.get_object()

        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")

        queryset = TipoCambio.objects.filter(pais=pais)

        if fecha_inicio:
            queryset = queryset.filter(fecha__gte=fecha_inicio)

        if fecha_fin:
            queryset = queryset.filter(fecha__lte=fecha_fin)

        queryset = queryset.order_by("-fecha")

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = TipoCambioSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TipoCambioSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action( detail=False, methods=["post"], url_path="sync-indicadores", permission_classes=[IsAdminUser])
    def sync_indicadores(self, request):

        call_command("sync_paises")
        call_command("sync_indicadores")

        return Response({
            "mensaje": "Sincronización de indicadores Finalizados"
        })