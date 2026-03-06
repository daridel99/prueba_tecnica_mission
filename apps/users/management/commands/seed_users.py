from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        users = [
            {
                "email": "admin@datapulse.com",
                "password": "DataPulse2026!",
                "username": "admin@datapulse",
                "nombre_completo": "Administrador",
                "rol": "ADMIN",
                "is_staff": True,
                "is_superuser": True
            },
            {
                "email": "analista@datapulse.com",
                "password": "DataPulse2026!",
                "username": "analista@datapulse",
                "nombre_completo": "Analista",
                "rol": "ANALISTA",
            },
            {
                "email": "viewer@datapulse.com",
                "password": "DataPulse2026!",
                "username": "viewer@datapulse",
                "nombre_completo": "Viewer",
                "rol": "VIEWER",
            }
        ]

        for u in users:

            if not User.objects.filter(email=u["email"]).exists():

                user = User.objects.create_user(
                    email=u["email"],
                    password=u["password"],
                    username=u["username"],
                    nombre_completo=u["nombre_completo"],
                    rol=u["rol"]
                )

                if u.get("is_staff"):
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()

                self.stdout.write(f"Usuario creado: {u['email']}")
