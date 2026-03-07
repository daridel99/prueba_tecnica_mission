from rest_framework.views import APIView
from rest_framework.response import Response
from apps.countries.models import Pais
from apps.alerts.models import Alerta
from apps.portfolios.models import Portafolio
from apps.risk.models import IndiceRiesgo
from apps.indicators.models import IndicadorEconomico
from django.db.models import Avg, Subquery, OuterRef


class DashboardResumen(APIView):
    def get(self, request):
        return Response({
            "total_paises": Pais.objects.filter(activo=True).count(),
            "alertas_activas": Alerta.objects.filter(leida=False).count(),
            "portafolios": Portafolio.objects.filter(usuario=request.user, activo=True).count(),
            "riesgo_promedio": IndiceRiesgo.objects.aggregate(promedio=Avg("indice_compuesto"))["promedio"]
        })


class DashboardMapa(APIView):
    def get(self, request):
        ultimo_riesgo = IndiceRiesgo.objects.filter(
            pais=OuterRef("pk")
        ).order_by("-fecha_calculo")
        paises = Pais.objects.filter(activo=True).annotate(
            riesgo=Subquery(ultimo_riesgo.values("indice_compuesto")[:1])
        )
        return Response([{
            "pais": p.nombre, "codigo": p.codigo_iso,
            "lat": p.latitud, "lng": p.longitud, "riesgo": p.riesgo
        } for p in paises])


class DashboardTendencias(APIView):
    def get(self, request):
        pais = request.query_params.get("pais")
        tipo = request.query_params.get("tipo")
        queryset = IndicadorEconomico.objects.values("pais__codigo_iso", "tipo", "anio", "valor")
        if pais:
            queryset = queryset.filter(pais__codigo_iso__in=pais.split(","))
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        queryset = queryset.order_by("anio")[:200]
        return Response([{
            "pais": i["pais__codigo_iso"], "tipo": i["tipo"],
            "anio": i["anio"], "valor": i["valor"]
        } for i in queryset])
