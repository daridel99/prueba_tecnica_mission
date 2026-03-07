from django.contrib.auth import get_user_model

User = get_user_model()


def seed_users():

    users = [
        {
            "email": "admin@datapulse.com",
            "username": "admin",
            "password": "DataPulse2026!",
            "nombre_completo": "Administrador",
            "rol": User.Roles.ADMIN
        },
        {
            "email": "analista@datapulse.com",
            "username": "analista",
            "password": "DataPulse2026!",
            "nombre_completo": "Analista",
            "rol": User.Roles.ANALISTA
        },
        {
            "email": "viewer@datapulse.com",
            "username": "viewer",
            "password": "DataPulse2026!",
            "nombre_completo": "Viewer",
            "rol": User.Roles.VIEWER
        }
    ]

    for u in users:

        if not User.objects.filter(email=u["email"]).exists():

            User.objects.create_user(
                email=u["email"],
                username=u["username"],
                password=u["password"],
                nombre_completo=u["nombre_completo"],
                rol=u["rol"]
            )