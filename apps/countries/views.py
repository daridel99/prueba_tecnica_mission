from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Pais
from .serializers import PaisSerializer


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticated]