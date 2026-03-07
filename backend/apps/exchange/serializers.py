from rest_framework import serializers
from .models import TipoCambio


class TipoCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCambio
        fields = "__all__"
        read_only_fields = ["id"]
