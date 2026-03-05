import requests
from django.core.management.base import BaseCommand
from apps.countries.models import Pais
from apps.indicators.models import IndicadorEconomico
from apps.exchange.models import TipoCambio
from datetime import date, datetime

WORLD_BANK_BASE = "https://api.worldbank.org/v2"


INDICADORES = {
    "NY.GDP.MKTP.CD": "PIB",
    "FP.CPI.TOTL.ZG": "INFLACION",
    "SL.UEM.TOTL.ZS": "DESEMPLEO",
    "NE.RSB.GNFS.ZS": "BALANZA_COMERCIAL",
    "GC.DOD.TOTL.GD.ZS": "DEUDA_PIB",
    "NY.GDP.PCAP.CD": "PIB_PERCAPITA",
}


PAISES = ["CO", "BR", "MX", "AR", "CL", "PE", "EC", "UY", "PY", "PA"]


class Command(BaseCommand):

    help = "Sincroniza indicadores económicos y tipo de cambio"

    def handle(self, *args, **kwargs):

        self.stdout.write("Sincronizando indicadores económicos...")

        for codigo in PAISES:

            pais = Pais.objects.filter(codigo_iso=codigo).first()

            if not pais:
                self.stdout.write(f"Pais {codigo} no existe en BD")
                continue

            for indicador_wb, campo in INDICADORES.items():

                url = f"{WORLD_BANK_BASE}/country/{codigo}/indicator/{indicador_wb}?date=2019:2023&format=json"

                response = requests.get(url)

                if response.status_code != 200:
                    continue

                data = response.json()

                if len(data) < 2:
                    continue

                for registro in data[1]:

                    if registro["value"] is None:
                        continue

                    anio = int(registro["date"])

                    indicador, created = IndicadorEconomico.objects.update_or_create(
                            pais=pais,
                            anio=anio,
                            tipo=campo.upper(),
                            defaults={
                                "valor": registro["value"],
                                "unidad": "N/A",
                                "fuente": "World Bank"
                            }
                        )

                    if not created:
                        setattr(indicador, campo, registro["value"])
                        indicador.save()

        self.stdout.write("Indicadores económicos sincronizados")

        self.sync_exchange()

    def sync_exchange(self):

        self.stdout.write("Sincronizando tipos de cambio...")

        url = "https://api.exchangerate-api.com/v4/latest/{}"

        monedas = {
            "CO": "COP",
            "BR": "BRL",
            "MX": "MXN",
            "AR": "ARS",
            "CL": "CLP",
            "PE": "PEN",
            "EC": "USD",
            "UY": "UYU",
            "PY": "PYG",
            "PA": "PAB",
        }

        for codigo, moneda in monedas.items():

            pais = Pais.objects.filter(codigo_iso=codigo).first()
            if not pais:
                continue

            try:
                response = requests.get(url.format(moneda))
                data = response.json()
            except Exception:
                continue

            rates = data.get("rates", {})
            tasa = rates.get("USD")

            if not tasa:
                continue

            fecha_str = data.get("date")

            if fecha_str:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            else:
                fecha = date.today()

            ultimo = (
                TipoCambio.objects
                .filter(pais=pais)
                .order_by("-fecha")[1:2]
                .first()
            )

            print(ultimo)

            variacion = None

            if ultimo:
                variacion = ((tasa - float(ultimo.tasa)) / float(ultimo.tasa)) * 100

            TipoCambio.objects.update_or_create(
                pais=pais,
                fecha=fecha,
                defaults={
                    "moneda_destino": "USD",
                    "tasa": tasa,
                    "variacion_porcentual": variacion,
                    "fuente": "ExchangeRate API"
                }
            )

        self.stdout.write(self.style.SUCCESS("Tipos de cambio sincronizados"))