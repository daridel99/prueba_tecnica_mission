from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="admin@test.com", username="admin_test",
            password="TestPass123!", nombre_completo="Admin Test", rol="ADMIN",
        )
        self.viewer = User.objects.create_user(
            email="viewer@test.com", username="viewer_test",
            password="TestPass123!", nombre_completo="Viewer Test", rol="VIEWER",
        )

    def _login(self, email, password="TestPass123!"):
        return self.client.post("/api/auth/login/", {"email": email, "password": password})

    def test_login_success(self):
        response = self._login("admin@test.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_wrong_password(self):
        response = self._login("admin@test.com", "WrongPass!")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_success(self):
        response = self.client.post("/api/auth/register/", {
            "email": "new@test.com", "username": "newuser",
            "password": "NewPass123!", "nombre_completo": "New User", "rol": "VIEWER",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_me_authenticated(self):
        token = self._login("admin@test.com").data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "admin@test.com")

    def test_me_unauthenticated(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_role_has_staff(self):
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)

    def test_viewer_no_staff(self):
        self.assertFalse(self.viewer.is_staff)
