from rest_framework import serializers
from .models import IndicadorEconomico


class IndicadorEconomicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorEconomico
        fields = "__all__"
        read_only_fields = ["id", "fecha_actualizacion"]
