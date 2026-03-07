from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import IndicadorEconomico
from .serializers import IndicadorEconomicoSerializer


class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = IndicadorEconomico.objects.all()
    serializer_class = IndicadorEconomicoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["pais", "tipo", "anio"]
    search_fields = ["tipo"]
    ordering_fields = ["anio", "valor", "tipo"]
