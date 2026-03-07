import logging
import requests
from django.core.management.base import BaseCommand
from apps.countries.models import Pais
from apps.indicators.models import IndicadorEconomico
from apps.exchange.models import TipoCambio
from apps.alerts.models import Alerta
from datetime import date, datetime

logger = logging.getLogger(__name__)

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
    help = "Sincroniza indicadores economicos y tipo de cambio"

    def handle(self, *args, **kwargs):
        self.stdout.write("Sincronizando indicadores economicos...")
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
                    IndicadorEconomico.objects.update_or_create(
                        pais=pais, anio=anio, tipo=campo.upper(),
                        defaults={
                            "valor": registro["value"],
                            "unidad": "N/A",
                            "fuente": "World Bank"
                        }
                    )
        self.stdout.write("Indicadores economicos sincronizados")
        self.sync_exchange()
        Alerta.objects.create(
            pais=None, tipo_alerta=Alerta.TipoAlerta.SISTEMA, severidad=Alerta.Severidad.INFO,
            titulo="Sincronizacion de datos completada",
            mensaje=f"Se actualizaron indicadores economicos y tipos de cambio para {len(PAISES)} paises.",
            leida=False
        )

    def sync_exchange(self):
        self.stdout.write("Sincronizando tipos de cambio...")
        url = "https://api.exchangerate-api.com/v4/latest/{}"
        monedas = {
            "CO": "COP", "BR": "BRL", "MX": "MXN", "AR": "ARS", "CL": "CLP",
            "PE": "PEN", "EC": "USD", "UY": "UYU", "PY": "PYG", "PA": "PAB",
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
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else date.today()
            ultimo = (
                TipoCambio.objects.filter(pais=pais)
                .exclude(fecha=fecha).order_by("-fecha").first()
            )
            variacion = None
            if ultimo:
                variacion = ((tasa - float(ultimo.tasa)) / float(ultimo.tasa)) * 100
            TipoCambio.objects.update_or_create(
                pais=pais, fecha=fecha,
                defaults={
                    "moneda_destino": "USD", "tasa": tasa,
                    "variacion_porcentual": variacion,
                    "fuente": "ExchangeRate API"
                }
            )
            if variacion is not None and abs(variacion) > 3:
                Alerta.objects.create(
                    pais=pais, tipo_alerta=Alerta.TipoAlerta.TIPO_CAMBIO, severidad=Alerta.Severidad.WARNING,
                    titulo=f"Variacion tipo de cambio > 3% en {pais.nombre}",
                    mensaje=f"El tipo de cambio de {pais.moneda_codigo}/USD vario {variacion:.2f}% en un dia.",
                    leida=False
                )
        self.stdout.write(self.style.SUCCESS("Tipos de cambio sincronizados"))
