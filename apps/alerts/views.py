from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Alerta
from .serializers import AlertaSerializer


class AlertaViewSet(viewsets.ModelViewSet):

    serializer_class = AlertaSerializer

    def get_queryset(self):
        user = self.request.user
        return Alerta.objects.filter(usuario=user)

    @action(detail=True, methods=["put"])
    def leer(self, request, pk=None):

        alerta = self.get_object()
        alerta.leida = True
        alerta.save()

        return Response({"status": "alerta marcada como leída"})

    @action(detail=False, methods=["put"], url_path="leer-todas")
    def leer_todas(self, request):

        qs = self.get_queryset()
        qs.update(leida=True)

        return Response({"status": "todas las alertas marcadas"})

    @action(detail=False, methods=["get"])
    def resumen(self, request):

        qs = self.get_queryset()

        data = {
            "total": qs.count(),
            "no_leidas": qs.filter(leida=False).count(),
            "info": qs.filter(severidad="INFO").count(),
            "warning": qs.filter(severidad="WARNING").count(),
            "critical": qs.filter(severidad="CRITICAL").count(),
        }

        return Response(data)