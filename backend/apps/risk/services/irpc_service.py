import statistics

from apps.indicators.models import IndicadorEconomico
from apps.exchange.models import TipoCambio
from apps.risk.models import IndiceRiesgo
from apps.alerts.models import Alerta
from django.utils import timezone


class IRPCService:

    @staticmethod
    def _fetch_indicators(pais):
        """Fetch all latest indicators for a country in a single query."""
        qs = (
            IndicadorEconomico.objects.filter(pais=pais)
            .order_by("tipo", "-anio")
            .distinct("tipo")
            .values_list("tipo", "valor", "anio")
        )
        # distinct("tipo") requires PostgreSQL; fallback for SQLite
        try:
            result = {row[0]: {"valor": float(row[1]), "anio": row[2]} for row in qs}
        except Exception:
            result = {}
            for tipo in ["PIB", "PIB_PERCAPITA", "INFLACION", "DESEMPLEO", "DEUDA_PIB", "BALANZA_COMERCIAL"]:
                ind = (
                    IndicadorEconomico.objects.filter(pais=pais, tipo=tipo)
                    .order_by("-anio").values_list("valor", "anio").first()
                )
                if ind:
                    result[tipo] = {"valor": float(ind[0]), "anio": ind[1]}
        return result

    @staticmethod
    def calcular_score_economico(indicators):
        score = 100
        pib_pc = indicators.get("PIB_PERCAPITA", {}).get("valor")
        if pib_pc is not None:
            if pib_pc < 3000: score -= 30
            elif pib_pc < 6000: score -= 15
            elif pib_pc < 12000: score -= 5
        inflacion = indicators.get("INFLACION", {}).get("valor")
        if inflacion is not None:
            if inflacion > 50: score -= 40
            elif inflacion > 10: score -= 25
            elif inflacion > 5: score -= 10
        desempleo = indicators.get("DESEMPLEO", {}).get("valor")
        if desempleo is not None:
            if desempleo > 15: score -= 25
            elif desempleo > 10: score -= 15
            elif desempleo > 7: score -= 5
        deuda = indicators.get("DEUDA_PIB", {}).get("valor")
        if deuda is not None:
            if deuda > 80: score -= 20
            elif deuda > 50: score -= 10
        return max(0, score)

    @staticmethod
    def calcular_score_cambiario(pais):
        score = 100
        cambios = list(
            TipoCambio.objects.filter(pais=pais).order_by("-fecha")[:30]
            .values_list("variacion_porcentual", flat=True)
        )
        variaciones = [float(v) for v in cambios if v is not None]
        if len(variaciones) < 2:
            return 50
        try:
            volatilidad = statistics.stdev(variaciones)
        except statistics.StatisticsError:
            volatilidad = 0
        if volatilidad > 3.0: score -= 40
        elif volatilidad > 1.5: score -= 25
        elif volatilidad > 0.5: score -= 10
        depreciacion = sum(variaciones)
        if depreciacion > 10: score -= 30
        elif depreciacion > 5: score -= 15
        elif depreciacion > 2: score -= 5
        return max(0, score)

    @staticmethod
    def calcular_score_estabilidad(pais, indicators):
        score = 100
        balanza = indicators.get("BALANZA_COMERCIAL", {}).get("valor")
        if balanza is not None:
            if balanza < -10: score -= 25
            elif balanza < -5: score -= 15
            elif balanza < 0: score -= 5

        pib_data = indicators.get("PIB", {})
        pib_actual = pib_data.get("valor")
        ultimo_anio = pib_data.get("anio")
        pib_anterior = None
        if ultimo_anio:
            prev = (
                IndicadorEconomico.objects.filter(pais=pais, tipo="PIB", anio=ultimo_anio - 1)
                .values_list("valor", flat=True).first()
            )
            if prev is not None:
                pib_anterior = float(prev)

        if pib_anterior and pib_actual and pib_anterior != 0:
            crecimiento = ((pib_actual - pib_anterior) / abs(pib_anterior)) * 100
            if crecimiento < -2: score -= 30
            elif crecimiento < 0: score -= 20
            elif crecimiento < 1: score -= 10

        indicadores_negativos = IRPCService.contar_indicadores_en_riesgo(indicators)
        score -= (indicadores_negativos * 5)
        return max(0, score)

    @staticmethod
    def calcular_indice_compuesto(score_economico, score_cambiario, score_estabilidad):
        return round(
            (score_economico * 0.40) + (score_cambiario * 0.30) + (score_estabilidad * 0.30), 2
        )

    @staticmethod
    def clasificar_riesgo(indice):
        if indice >= 75: return "BAJO"
        elif indice >= 50: return "MODERADO"
        elif indice >= 25: return "ALTO"
        else: return "CRITICO"

    @staticmethod
    def calcular_irpc(pais):
        indicators = IRPCService._fetch_indicators(pais)
        score_economico = IRPCService.calcular_score_economico(indicators)
        score_cambiario = IRPCService.calcular_score_cambiario(pais)
        score_estabilidad = IRPCService.calcular_score_estabilidad(pais, indicators)
        indice = IRPCService.calcular_indice_compuesto(score_economico, score_cambiario, score_estabilidad)
        nivel = IRPCService.clasificar_riesgo(indice)
        indice_anterior = IndiceRiesgo.objects.filter(pais=pais).order_by("-fecha_calculo").first()
        indice_obj, created = IndiceRiesgo.objects.update_or_create(
            pais=pais, fecha_calculo=timezone.now().date(),
            defaults={
                "score_economico": score_economico, "score_cambiario": score_cambiario,
                "score_estabilidad": score_estabilidad, "indice_compuesto": indice,
                "nivel_riesgo": nivel,
                "detalle_calculo": {"economico": score_economico, "cambiario": score_cambiario, "estabilidad": score_estabilidad}
            }
        )
        if indice < 25:
            Alerta.objects.create(
                pais=pais, tipo_alerta="RIESGO", severidad="CRITICAL",
                titulo="Riesgo critico detectado",
                mensaje=f"El IRPC de {pais.nombre} cayo a {indice:.2f}", leida=False
            )
        inflacion = indicators.get("INFLACION", {}).get("valor")
        if inflacion is not None and inflacion > 50:
            Alerta.objects.create(
                pais=pais, tipo_alerta="INDICADOR", severidad="CRITICAL",
                titulo=f"Hiperinflacion detectada en {pais.nombre}",
                mensaje=f"La inflacion de {pais.nombre} es de {inflacion:.2f}%, superando el umbral de 50%.",
                leida=False
            )
        if indice_anterior:
            diferencia = indice_anterior.indice_compuesto - indice
            if diferencia > 15:
                Alerta.objects.create(
                    pais=pais, tipo_alerta="RIESGO", severidad="WARNING",
                    titulo="Caida fuerte en el indice de riesgo",
                    mensaje=f"{pais.nombre} cayo {diferencia:.2f} puntos en el IRPC", leida=False
                )
        return indice_obj

    @staticmethod
    def contar_indicadores_en_riesgo(indicators):
        count = 0
        inflacion = indicators.get("INFLACION", {}).get("valor")
        if inflacion is not None and inflacion > 10: count += 1
        desempleo = indicators.get("DESEMPLEO", {}).get("valor")
        if desempleo is not None and desempleo > 10: count += 1
        deuda = indicators.get("DEUDA_PIB", {}).get("valor")
        if deuda is not None and deuda > 50: count += 1
        balanza = indicators.get("BALANZA_COMERCIAL", {}).get("valor")
        if balanza is not None and balanza < -5: count += 1
        pib_pc = indicators.get("PIB_PERCAPITA", {}).get("valor")
        if pib_pc is not None and pib_pc < 6000: count += 1
        return count

    @staticmethod
    def recalcular_todos():
        from apps.countries.models import Pais
        paises = Pais.objects.filter(activo=True)
        resultados = []
        for pais in paises:
            indice = IRPCService.calcular_irpc(pais)
            resultados.append({"pais": pais.codigo_iso, "indice": indice.indice_compuesto})
        return resultados
