from datetime import date

from django.db.models import Count, Q, Sum
from rest_framework import serializers

from .models import Portafolio, Posicion


class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        fields = "__all__"
        read_only_fields = ["id", "portafolio"]

    def validate_monto_inversion_usd(self, value):
        if value < 1000:
            raise serializers.ValidationError("El monto minimo de inversion es $1,000 USD.")
        if value > 10_000_000:
            raise serializers.ValidationError("El monto maximo de inversion es $10,000,000 USD.")
        return value

    def validate_fecha_entrada(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de entrada no puede ser futura.")
        return value

    def validate(self, attrs):
        pais = attrs.get("pais")
        tipo_activo = attrs.get("tipo_activo")
        monto = attrs.get("monto_inversion_usd")
        portafolio = self.context.get("portafolio")

        if not portafolio or not pais or not monto:
            return attrs

        # No MONEDA if country currency is USD
        if tipo_activo == Posicion.TipoActivo.MONEDA and pais.moneda_codigo == "USD":
            raise serializers.ValidationError(
                "No se puede crear una posicion de tipo MONEDA en un pais con moneda USD."
            )

        # Single query for both validations
        exclude_pk = self.instance.pk if self.instance else None
        stats = Posicion.objects.filter(
            portafolio=portafolio, fecha_salida__isnull=True
        ).exclude(pk=exclude_pk).aggregate(
            same_count=Count("id", filter=Q(pais=pais, tipo_activo=tipo_activo)),
            total=Sum("monto_inversion_usd")
        )

        # Max 2 active positions of same tipo_activo + same country
        if stats["same_count"] >= 2:
            raise serializers.ValidationError(
                f"Ya existen 2 posiciones activas de tipo {tipo_activo} en {pais.nombre}."
            )

        # Total portfolio <= $50,000,000
        total_actual = stats["total"] or 0
        if total_actual + monto > 50_000_000:
            raise serializers.ValidationError(
                f"El total del portafolio no puede superar $50,000,000 USD. "
                f"Actual: ${total_actual:,.2f}, nuevo monto: ${monto:,.2f}."
            )

        return attrs


class PortafolioSerializer(serializers.ModelSerializer):
    posiciones = PosicionSerializer(many=True, read_only=True)

    class Meta:
        model = Portafolio
        fields = ["id", "nombre", "descripcion", "usuario", "fecha_creacion",
                  "fecha_modificacion", "activo", "es_publico", "posiciones"]
        read_only_fields = ["id", "usuario", "fecha_creacion", "fecha_modificacion"]

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return value
