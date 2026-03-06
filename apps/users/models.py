from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ANALISTA = "ANALISTA", "Analista"
        VIEWER = "VIEWER", "Viewer"

    email = models.EmailField(unique=True)
    nombre_completo = models.CharField(max_length=255)
    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.VIEWER
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.is_active = self.activo
        if self.rol == self.Roles.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)