from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        "email",
        "nombre_completo",
        "rol",
        "is_staff",
        "activo",
    )

    list_filter = ("rol", "activo", "is_staff")
    search_fields = ("email", "nombre_completo")
    ordering = ("email",)
    
    fieldsets = UserAdmin.fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "nombre_completo",
                    "rol",
                    "activo",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "email",
                    "nombre_completo",
                    "rol",
                    "activo",
                )
            },
        ),
    )