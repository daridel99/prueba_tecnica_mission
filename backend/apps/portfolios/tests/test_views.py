from decimal import Decimal
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.countries.models import Pais
from apps.portfolios.models import Portafolio, Posicion

User = get_user_model()


class PortafolioViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.pais = Pais.objects.create(
            codigo_iso="TS", nombre="TestPais", moneda_codigo="TST",
            moneda_nombre="Test", region="ANDINA", latitud=4.0, longitud=-74.0, poblacion=50000000,
        )
        self.analista = User.objects.create_user(
            email="analista_p@test.com", username="analista_port",
            password="TestPass123!", nombre_completo="Analista", rol="ANALISTA",
        )
        self.viewer = User.objects.create_user(
            email="viewer_p@test.com", username="viewer_port",
            password="TestPass123!", nombre_completo="Viewer", rol="VIEWER",
        )
        self._auth_as(self.analista)

    def _auth_as(self, user):
        response = self.client.post("/api/auth/login/", {"email": user.email, "password": "TestPass123!"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_create_portafolio(self):
        response = self.client.post("/api/portafolios/", {"nombre": "Test", "descripcion": "Desc", "es_publico": True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_viewer_cannot_create(self):
        self._auth_as(self.viewer)
        response = self.client.post("/api/portafolios/", {"nombre": "Fail"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_soft_delete(self):
        p = Portafolio.objects.create(nombre="ToDelete", usuario=self.analista)
        response = self.client.delete(f"/api/portafolios/{p.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        p.refresh_from_db()
        self.assertFalse(p.activo)

    def test_resumen(self):
        p = Portafolio.objects.create(nombre="Resumen Test", usuario=self.analista)
        Posicion.objects.create(
            portafolio=p, pais=self.pais, tipo_activo="RENTA_FIJA",
            monto_inversion_usd=Decimal("100000"), fecha_entrada=date.today(),
        )
        response = self.client.get(f"/api/portafolios/{p.id}/resumen/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_posiciones"], 1)
        self.assertEqual(response.data["total_invertido"], 100000.0)
