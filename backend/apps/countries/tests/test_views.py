from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.countries.models import Pais

User = get_user_model()


class PaisViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@test.com", username="user_test",
            password="TestPass123!", nombre_completo="User Test", rol="ANALISTA",
        )
        response = self.client.post("/api/auth/login/", {"email": "user@test.com", "password": "TestPass123!"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        Pais.objects.create(
            codigo_iso="CO", nombre="Colombia", moneda_codigo="COP",
            moneda_nombre="Peso colombiano", region="ANDINA", latitud=4.57, longitud=-74.3, poblacion=51000000,
        )
        Pais.objects.create(
            codigo_iso="BR", nombre="Brazil", moneda_codigo="BRL",
            moneda_nombre="Real brasileno", region="CONO_SUR", latitud=-14.24, longitud=-51.93, poblacion=214000000,
        )

    def test_list_paises(self):
        response = self.client.get("/api/paises/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_pais_by_codigo(self):
        response = self.client.get("/api/paises/CO/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], "Colombia")

    def test_filter_by_region(self):
        response = self.client.get("/api/paises/?region=ANDINA")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_search(self):
        response = self.client.get("/api/paises/?search=Braz")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_unauthenticated(self):
        client = APIClient()
        response = client.get("/api/paises/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
