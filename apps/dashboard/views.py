from rest_framework.views import APIView
from rest_framework.response import Response
from apps.countries.models import Pais
from apps.alerts.models import Alerta
from apps.portfolios.models import Portafolio
from apps.risk.models import IndiceRiesgo
from apps.indicators.models import IndicadorEconomico
from django.db.models import Max
from django.db.models import Avg


class DashboardResumen(APIView):

    def get(self, request):

        data = {
            "total_paises": Pais.objects.count(),
            "alertas_activas": Alerta.objects.filter(leida=False).count(),
            "portafolios": Portafolio.objects.count(),
            "riesgo_promedio": IndiceRiesgo.objects.aggregate(promedio=Avg("indice_compuesto"))
                    ["promedio"] }

        return Response(data)


class DashboardMapa(APIView):

    def get(self, request):

        paises = Pais.objects.all()

        data = []

        for p in paises:

            riesgo = (
                IndiceRiesgo.objects.filter(pais=p)
                .order_by("-fecha_calculo")
                .first()
            )

            data.append({
                "pais": p.nombre,
                "codigo": p.codigo_iso,
                "lat": p.latitud,
                "lng": p.longitud,
                "riesgo": riesgo.indice_compuesto if riesgo else None
            })

        return Response(data)
    

class DashboardTendencias(APIView):

    def get(self, request):

        indicadores = (
            IndicadorEconomico.objects
            .values("pais__codigo_iso", "tipo", "anio", "valor")
            .order_by("-anio")[:100]
        )

        data = []

        for i in indicadores:

            data.append({
                "pais": i["pais__codigo_iso"],
                "tipo": i["tipo"],
                "anio": i["anio"],
                "valor": i["valor"]
            })

        return Response(data)