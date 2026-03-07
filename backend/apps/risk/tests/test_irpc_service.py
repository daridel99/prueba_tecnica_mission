from decimal import Decimal
from datetime import date, timedelta
import random

from django.test import TestCase

from apps.countries.models import Pais
from apps.indicators.models import IndicadorEconomico
from apps.exchange.models import TipoCambio
from apps.risk.models import IndiceRiesgo
from apps.risk.services.irpc_service import IRPCService


class IRPCServiceTest(TestCase):

    def setUp(self):
        self.pais = Pais.objects.create(
            codigo_iso="TS", nombre="TestPais", moneda_codigo="TST",
            moneda_nombre="Test Moneda", region="ANDINA",
            latitud=4.0, longitud=-74.0, poblacion=50000000,
        )

    def _create_indicator(self, tipo, valor, anio=2023):
        IndicadorEconomico.objects.update_or_create(
            pais=self.pais, tipo=tipo, anio=anio,
            defaults={"valor": Decimal(str(valor)), "unidad": "N/A", "fuente": "MANUAL"}
        )

    def _create_exchange_rates(self, days=30, base_rate=4000.0, variation=0.5):
        today = date.today()
        prev_rate = None
        for i in range(days, -1, -1):
            rate = base_rate * (1 + random.uniform(-variation, variation) / 100)
            var = None
            if prev_rate:
                var = ((rate - prev_rate) / prev_rate) * 100
            TipoCambio.objects.create(
                pais=self.pais, fecha=today - timedelta(days=i),
                moneda_destino="USD", tasa=Decimal(str(round(rate, 6))),
                variacion_porcentual=Decimal(str(round(var, 3))) if var else None,
                fuente="TEST",
            )
            prev_rate = rate

    def test_score_economico_perfect(self):
        self._create_indicator("PIB_PERCAPITA", 15000)
        self._create_indicator("INFLACION", 3.0)
        self._create_indicator("DESEMPLEO", 5.0)
        self._create_indicator("DEUDA_PIB", 30.0)
        indicators = IRPCService._fetch_indicators(self.pais)
        self.assertEqual(IRPCService.calcular_score_economico(indicators), 100)

    def test_score_economico_worst_case(self):
        self._create_indicator("PIB_PERCAPITA", 2500)
        self._create_indicator("INFLACION", 55)
        self._create_indicator("DESEMPLEO", 16)
        self._create_indicator("DEUDA_PIB", 85)
        indicators = IRPCService._fetch_indicators(self.pais)
        self.assertEqual(IRPCService.calcular_score_economico(indicators), 0)

    def test_score_economico_colombia_like(self):
        self._create_indicator("PIB_PERCAPITA", 6428)
        self._create_indicator("INFLACION", 11.7)
        self._create_indicator("DESEMPLEO", 10.1)
        self._create_indicator("DEUDA_PIB", 55.2)
        indicators = IRPCService._fetch_indicators(self.pais)
        self.assertEqual(IRPCService.calcular_score_economico(indicators), 45)

    def test_score_cambiario_no_data(self):
        self.assertEqual(IRPCService.calcular_score_cambiario(self.pais), 50)

    def test_clasificar_riesgo(self):
        self.assertEqual(IRPCService.clasificar_riesgo(80), "BAJO")
        self.assertEqual(IRPCService.clasificar_riesgo(60), "MODERADO")
        self.assertEqual(IRPCService.clasificar_riesgo(30), "ALTO")
        self.assertEqual(IRPCService.clasificar_riesgo(10), "CRITICO")

    def test_calcular_indice_compuesto(self):
        self.assertEqual(IRPCService.calcular_indice_compuesto(45, 90, 80), 69.0)

    def test_calcular_irpc_creates_record(self):
        self._create_indicator("PIB_PERCAPITA", 10000)
        self._create_indicator("INFLACION", 5.0)
        self._create_indicator("DESEMPLEO", 7.0)
        self._create_indicator("DEUDA_PIB", 40.0)
        self._create_indicator("BALANZA_COMERCIAL", 2.0)
        self._create_exchange_rates()
        result = IRPCService.calcular_irpc(self.pais)
        self.assertIsInstance(result, IndiceRiesgo)
        self.assertGreaterEqual(result.indice_compuesto, 0)
        self.assertLessEqual(result.indice_compuesto, 100)
