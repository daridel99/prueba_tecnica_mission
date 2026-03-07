import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

from apps.countries.models import Pais
from apps.indicators.models import IndicadorEconomico
from apps.exchange.models import TipoCambio
from apps.portfolios.models import Portafolio, Posicion
from apps.alerts.models import Alerta
from apps.risk.services.irpc_service import IRPCService

User = get_user_model()

PAISES_DATA = [
    {"codigo_iso": "CO", "nombre": "Colombia", "moneda_codigo": "COP", "moneda_nombre": "Peso colombiano", "region": "ANDINA", "latitud": 4.5709, "longitud": -74.2973, "poblacion": 51874024},
    {"codigo_iso": "BR", "nombre": "Brazil", "moneda_codigo": "BRL", "moneda_nombre": "Real brasileno", "region": "CONO_SUR", "latitud": -14.235, "longitud": -51.9253, "poblacion": 214326223},
    {"codigo_iso": "MX", "nombre": "Mexico", "moneda_codigo": "MXN", "moneda_nombre": "Peso mexicano", "region": "CENTROAMERICA", "latitud": 23.6345, "longitud": -102.5528, "poblacion": 128901000},
    {"codigo_iso": "AR", "nombre": "Argentina", "moneda_codigo": "ARS", "moneda_nombre": "Peso argentino", "region": "CONO_SUR", "latitud": -38.4161, "longitud": -63.6167, "poblacion": 45376763},
    {"codigo_iso": "CL", "nombre": "Chile", "moneda_codigo": "CLP", "moneda_nombre": "Peso chileno", "region": "CONO_SUR", "latitud": -35.6751, "longitud": -71.543, "poblacion": 19491616},
    {"codigo_iso": "PE", "nombre": "Peru", "moneda_codigo": "PEN", "moneda_nombre": "Sol peruano", "region": "ANDINA", "latitud": -9.19, "longitud": -75.0152, "poblacion": 33359418},
    {"codigo_iso": "EC", "nombre": "Ecuador", "moneda_codigo": "USD", "moneda_nombre": "Dolar estadounidense", "region": "ANDINA", "latitud": -1.8312, "longitud": -78.1834, "poblacion": 17643060},
    {"codigo_iso": "UY", "nombre": "Uruguay", "moneda_codigo": "UYU", "moneda_nombre": "Peso uruguayo", "region": "CONO_SUR", "latitud": -32.5228, "longitud": -55.7658, "poblacion": 3473727},
    {"codigo_iso": "PY", "nombre": "Paraguay", "moneda_codigo": "PYG", "moneda_nombre": "Guarani", "region": "CONO_SUR", "latitud": -23.4425, "longitud": -58.4438, "poblacion": 7132538},
    {"codigo_iso": "PA", "nombre": "Panama", "moneda_codigo": "PAB", "moneda_nombre": "Balboa", "region": "CENTROAMERICA", "latitud": 8.538, "longitud": -80.7821, "poblacion": 4314767},
]

INDICADORES_DATA = {
    "CO": {
        2021: {"PIB": 314464000000, "INFLACION": 3.5, "DESEMPLEO": 13.7, "BALANZA_COMERCIAL": -6.2, "DEUDA_PIB": 64.5, "PIB_PERCAPITA": 6104},
        2022: {"PIB": 343622000000, "INFLACION": 10.2, "DESEMPLEO": 11.2, "BALANZA_COMERCIAL": -5.8, "DEUDA_PIB": 60.1, "PIB_PERCAPITA": 6624},
        2023: {"PIB": 335835000000, "INFLACION": 11.7, "DESEMPLEO": 10.1, "BALANZA_COMERCIAL": -4.3, "DEUDA_PIB": 55.2, "PIB_PERCAPITA": 6428},
    },
    "BR": {
        2021: {"PIB": 1608981000000, "INFLACION": 8.3, "DESEMPLEO": 13.2, "BALANZA_COMERCIAL": 3.1, "DEUDA_PIB": 78.3, "PIB_PERCAPITA": 7519},
        2022: {"PIB": 1920096000000, "INFLACION": 9.3, "DESEMPLEO": 9.3, "BALANZA_COMERCIAL": 2.8, "DEUDA_PIB": 73.5, "PIB_PERCAPITA": 8918},
        2023: {"PIB": 2173000000000, "INFLACION": 4.6, "DESEMPLEO": 7.8, "BALANZA_COMERCIAL": 4.2, "DEUDA_PIB": 74.4, "PIB_PERCAPITA": 10025},
    },
    "MX": {
        2021: {"PIB": 1293038000000, "INFLACION": 5.7, "DESEMPLEO": 4.1, "BALANZA_COMERCIAL": -1.2, "DEUDA_PIB": 52.1, "PIB_PERCAPITA": 10046},
        2022: {"PIB": 1414187000000, "INFLACION": 7.9, "DESEMPLEO": 3.3, "BALANZA_COMERCIAL": -2.1, "DEUDA_PIB": 49.4, "PIB_PERCAPITA": 10948},
        2023: {"PIB": 1322740000000, "INFLACION": 5.5, "DESEMPLEO": 2.8, "BALANZA_COMERCIAL": -0.8, "DEUDA_PIB": 46.8, "PIB_PERCAPITA": 10218},
    },
    "AR": {
        2021: {"PIB": 487227000000, "INFLACION": 48.4, "DESEMPLEO": 8.7, "BALANZA_COMERCIAL": 1.5, "DEUDA_PIB": 80.9, "PIB_PERCAPITA": 10636},
        2022: {"PIB": 632770000000, "INFLACION": 72.4, "DESEMPLEO": 6.8, "BALANZA_COMERCIAL": -0.3, "DEUDA_PIB": 84.7, "PIB_PERCAPITA": 13709},
        2023: {"PIB": 621833000000, "INFLACION": 133.5, "DESEMPLEO": 5.7, "BALANZA_COMERCIAL": 1.8, "DEUDA_PIB": 89.5, "PIB_PERCAPITA": 13432},
    },
    "CL": {
        2021: {"PIB": 317059000000, "INFLACION": 4.5, "DESEMPLEO": 8.9, "BALANZA_COMERCIAL": 5.2, "DEUDA_PIB": 36.3, "PIB_PERCAPITA": 16265},
        2022: {"PIB": 301025000000, "INFLACION": 11.6, "DESEMPLEO": 7.9, "BALANZA_COMERCIAL": -3.1, "DEUDA_PIB": 38.0, "PIB_PERCAPITA": 15398},
        2023: {"PIB": 335533000000, "INFLACION": 7.6, "DESEMPLEO": 8.5, "BALANZA_COMERCIAL": 2.4, "DEUDA_PIB": 39.2, "PIB_PERCAPITA": 17094},
    },
    "PE": {
        2021: {"PIB": 223250000000, "INFLACION": 3.9, "DESEMPLEO": 5.1, "BALANZA_COMERCIAL": 6.3, "DEUDA_PIB": 36.0, "PIB_PERCAPITA": 6692},
        2022: {"PIB": 242632000000, "INFLACION": 7.9, "DESEMPLEO": 4.4, "BALANZA_COMERCIAL": 2.1, "DEUDA_PIB": 34.1, "PIB_PERCAPITA": 7232},
        2023: {"PIB": 264636000000, "INFLACION": 6.3, "DESEMPLEO": 4.6, "BALANZA_COMERCIAL": 4.8, "DEUDA_PIB": 33.5, "PIB_PERCAPITA": 7860},
    },
    "EC": {
        2021: {"PIB": 106166000000, "INFLACION": 1.9, "DESEMPLEO": 5.2, "BALANZA_COMERCIAL": -0.5, "DEUDA_PIB": 62.1, "PIB_PERCAPITA": 5965},
        2022: {"PIB": 115049000000, "INFLACION": 3.5, "DESEMPLEO": 4.4, "BALANZA_COMERCIAL": 1.2, "DEUDA_PIB": 57.4, "PIB_PERCAPITA": 6432},
        2023: {"PIB": 118845000000, "INFLACION": 2.2, "DESEMPLEO": 3.8, "BALANZA_COMERCIAL": 0.8, "DEUDA_PIB": 53.8, "PIB_PERCAPITA": 6612},
    },
    "UY": {
        2021: {"PIB": 59320000000, "INFLACION": 7.7, "DESEMPLEO": 9.3, "BALANZA_COMERCIAL": -0.8, "DEUDA_PIB": 61.4, "PIB_PERCAPITA": 17021},
        2022: {"PIB": 71177000000, "INFLACION": 8.3, "DESEMPLEO": 7.9, "BALANZA_COMERCIAL": -1.5, "DEUDA_PIB": 57.8, "PIB_PERCAPITA": 20381},
        2023: {"PIB": 77241000000, "INFLACION": 5.1, "DESEMPLEO": 8.3, "BALANZA_COMERCIAL": -0.3, "DEUDA_PIB": 55.2, "PIB_PERCAPITA": 22108},
    },
    "PY": {
        2021: {"PIB": 38987000000, "INFLACION": 4.8, "DESEMPLEO": 7.7, "BALANZA_COMERCIAL": -8.2, "DEUDA_PIB": 36.8, "PIB_PERCAPITA": 5415},
        2022: {"PIB": 41721000000, "INFLACION": 8.1, "DESEMPLEO": 6.8, "BALANZA_COMERCIAL": -7.1, "DEUDA_PIB": 38.5, "PIB_PERCAPITA": 5776},
        2023: {"PIB": 43009000000, "INFLACION": 4.5, "DESEMPLEO": 6.1, "BALANZA_COMERCIAL": -5.5, "DEUDA_PIB": 37.2, "PIB_PERCAPITA": 5941},
    },
    "PA": {
        2021: {"PIB": 63605000000, "INFLACION": 1.6, "DESEMPLEO": 10.2, "BALANZA_COMERCIAL": -12.3, "DEUDA_PIB": 66.2, "PIB_PERCAPITA": 14617},
        2022: {"PIB": 76522000000, "INFLACION": 2.9, "DESEMPLEO": 7.4, "BALANZA_COMERCIAL": -9.8, "DEUDA_PIB": 58.2, "PIB_PERCAPITA": 17525},
        2023: {"PIB": 83382000000, "INFLACION": 1.5, "DESEMPLEO": 6.8, "BALANZA_COMERCIAL": -8.1, "DEUDA_PIB": 53.4, "PIB_PERCAPITA": 19043},
    },
}

EXCHANGE_RATES = {
    "CO": 4150.0, "BR": 5.05, "MX": 17.2, "AR": 810.0, "CL": 880.0,
    "PE": 3.72, "EC": 1.0, "UY": 39.5, "PY": 7350.0, "PA": 1.0,
}

UNIDAD_MAP = {
    "PIB": "USD", "INFLACION": "PORCENTAJE", "DESEMPLEO": "PORCENTAJE",
    "BALANZA_COMERCIAL": "PORCENTAJE", "DEUDA_PIB": "PORCENTAJE", "PIB_PERCAPITA": "USD",
}


class Command(BaseCommand):
    help = "Carga datos de prueba completos"

    def handle(self, *args, **kwargs):
        self.stdout.write("Ejecutando seed_users...")
        call_command("seed_users")
        self.stdout.write("Creando paises...")
        self.seed_paises()
        self.stdout.write("Creando indicadores economicos...")
        self.seed_indicadores()
        self.stdout.write("Creando tipos de cambio...")
        self.seed_tipos_cambio()
        self.stdout.write("Calculando indices de riesgo...")
        self.seed_riesgo()
        self.stdout.write("Creando portafolios de ejemplo...")
        self.seed_portafolios()
        self.stdout.write("Creando alertas de ejemplo...")
        self.seed_alertas()
        self.stdout.write(self.style.SUCCESS("Seed data completado exitosamente"))

    def seed_paises(self):
        for data in PAISES_DATA:
            Pais.objects.update_or_create(
                codigo_iso=data["codigo_iso"],
                defaults={k: v for k, v in data.items() if k != "codigo_iso"}
            )

    def seed_indicadores(self):
        paises = {p.codigo_iso: p for p in Pais.objects.filter(codigo_iso__in=INDICADORES_DATA.keys())}
        existing = set(
            IndicadorEconomico.objects.filter(fuente="MANUAL")
            .values_list("pais__codigo_iso", "anio", "tipo")
        )
        to_create = []
        for codigo, anios in INDICADORES_DATA.items():
            pais = paises[codigo]
            for anio, indicadores in anios.items():
                for tipo, valor in indicadores.items():
                    if (codigo, anio, tipo) not in existing:
                        to_create.append(IndicadorEconomico(
                            pais=pais, anio=anio, tipo=tipo,
                            valor=Decimal(str(valor)), unidad=UNIDAD_MAP.get(tipo, "N/A"), fuente="MANUAL"
                        ))
        if to_create:
            IndicadorEconomico.objects.bulk_create(to_create, ignore_conflicts=True)

    def seed_tipos_cambio(self):
        today = date.today()
        paises = {p.codigo_iso: p for p in Pais.objects.filter(codigo_iso__in=EXCHANGE_RATES.keys())}
        existing = set(
            TipoCambio.objects.filter(fuente="MANUAL")
            .values_list("pais__codigo_iso", "fecha")
        )
        to_create = []
        for codigo, base_rate in EXCHANGE_RATES.items():
            pais = paises[codigo]
            tasa_anterior = None
            for i in range(30, -1, -1):
                fecha = today - timedelta(days=i)
                tasa = base_rate * (1 + random.uniform(-1.5, 1.5) / 100)
                variacion = None
                if tasa_anterior:
                    variacion = ((tasa - tasa_anterior) / tasa_anterior) * 100
                if (codigo, fecha) not in existing:
                    to_create.append(TipoCambio(
                        pais=pais, fecha=fecha, moneda_destino="USD",
                        tasa=Decimal(str(round(tasa, 6))),
                        variacion_porcentual=Decimal(str(round(variacion, 3))) if variacion else None,
                        fuente="MANUAL",
                    ))
                tasa_anterior = tasa
        if to_create:
            TipoCambio.objects.bulk_create(to_create, ignore_conflicts=True)

    def seed_riesgo(self):
        for pais in Pais.objects.filter(activo=True):
            IRPCService.calcular_irpc(pais)

    def seed_portafolios(self):
        analista = User.objects.filter(rol="ANALISTA").first()
        admin = User.objects.filter(rol="ADMIN").first()
        if not analista or not admin:
            return
        p1, _ = Portafolio.objects.update_or_create(
            usuario=analista, nombre="Portafolio Latam Growth",
            defaults={"descripcion": "Portafolio enfocado en mercados emergentes de Latinoamerica", "es_publico": True, "activo": True}
        )
        for pos in [
            {"pais": "BR", "tipo_activo": "RENTA_VARIABLE", "monto": 150000, "notas": "Acciones sector tecnologia"},
            {"pais": "MX", "tipo_activo": "RENTA_FIJA", "monto": 100000, "notas": "Bonos gobierno mexicano"},
            {"pais": "CL", "tipo_activo": "COMMODITIES", "monto": 75000, "notas": "Cobre y litio"},
            {"pais": "CO", "tipo_activo": "RENTA_VARIABLE", "monto": 80000, "notas": "Ecopetrol y bancolombia"},
            {"pais": "PE", "tipo_activo": "COMMODITIES", "monto": 60000, "notas": "Mineria de oro y plata"},
        ]:
            pais = Pais.objects.get(codigo_iso=pos["pais"])
            Posicion.objects.update_or_create(
                portafolio=p1, pais=pais, tipo_activo=pos["tipo_activo"],
                defaults={"monto_inversion_usd": Decimal(str(pos["monto"])), "fecha_entrada": date.today() - timedelta(days=random.randint(30, 180)), "notas": pos["notas"]}
            )
        p2, _ = Portafolio.objects.update_or_create(
            usuario=admin, nombre="Portafolio Conservador",
            defaults={"descripcion": "Portafolio de bajo riesgo enfocado en renta fija", "es_publico": False, "activo": True}
        )
        for pos in [
            {"pais": "UY", "tipo_activo": "RENTA_FIJA", "monto": 200000, "notas": "Bonos uruguayos"},
            {"pais": "PA", "tipo_activo": "RENTA_FIJA", "monto": 120000, "notas": "Bonos Panama canal"},
            {"pais": "CL", "tipo_activo": "RENTA_FIJA", "monto": 180000, "notas": "Bonos Chile soberanos"},
        ]:
            pais = Pais.objects.get(codigo_iso=pos["pais"])
            Posicion.objects.update_or_create(
                portafolio=p2, pais=pais, tipo_activo=pos["tipo_activo"],
                defaults={"monto_inversion_usd": Decimal(str(pos["monto"])), "fecha_entrada": date.today() - timedelta(days=random.randint(30, 180)), "notas": pos["notas"]}
            )

    def seed_alertas(self):
        co = Pais.objects.filter(codigo_iso="CO").first()
        ar = Pais.objects.filter(codigo_iso="AR").first()
        br = Pais.objects.filter(codigo_iso="BR").first()
        if not co or not ar or not br:
            return
        for a in [
            {"pais": ar, "tipo_alerta": "INDICADOR", "severidad": "CRITICAL", "titulo": "Hiperinflacion en Argentina", "mensaje": "La inflacion de Argentina supera el 133%."},
            {"pais": co, "tipo_alerta": "TIPO_CAMBIO", "severidad": "WARNING", "titulo": "Volatilidad en peso colombiano", "mensaje": "El COP/USD muestra variaciones superiores al 3%."},
            {"pais": br, "tipo_alerta": "RIESGO", "severidad": "INFO", "titulo": "Mejora en indice de riesgo de Brasil", "mensaje": "El IRPC de Brasil mejoro 5 puntos."},
            {"pais": co, "tipo_alerta": "INDICADOR", "severidad": "INFO", "titulo": "Datos actualizados", "mensaje": "Se actualizaron los indicadores economicos de Colombia para 2023."},
        ]:
            Alerta.objects.get_or_create(titulo=a["titulo"], defaults=a)
