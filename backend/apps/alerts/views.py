from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Case, When, IntegerField
from .models import Alerta
from .serializers import AlertaSerializer


class AlertaViewSet(viewsets.ModelViewSet):
    serializer_class = AlertaSerializer
    filterset_fields = ["tipo_alerta", "severidad", "leida"]
    search_fields = ["titulo", "mensaje"]
    ordering_fields = ["fecha_creacion", "severidad"]

    def get_queryset(self):
        user = self.request.user
        return Alerta.objects.filter(Q(usuario=user) | Q(usuario__isnull=True))

    @action(detail=True, methods=["put"])
    def leer(self, request, pk=None):
        alerta = self.get_object()
        alerta.leida = True
        alerta.save()
        return Response({"status": "alerta marcada como leida"})

    @action(detail=False, methods=["put"], url_path="leer-todas")
    def leer_todas(self, request):
        self.get_queryset().update(leida=True)
        return Response({"status": "todas las alertas marcadas"})

    @action(detail=False, methods=["get"])
    def resumen(self, request):
        agg = self.get_queryset().aggregate(
            total=Count("id"),
            no_leidas=Count(Case(When(leida=False, then=1), output_field=IntegerField())),
            info=Count(Case(When(severidad="INFO", then=1), output_field=IntegerField())),
            warning=Count(Case(When(severidad="WARNING", then=1), output_field=IntegerField())),
            critical=Count(Case(When(severidad="CRITICAL", then=1), output_field=IntegerField())),
        )
        return Response(agg)
