from rest_framework import serializers
from .models import IndicadorEconomico


class IndicadorEconomicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorEconomico
        fields = "__all__"