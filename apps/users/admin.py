from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "nombre_completo", "rol", "is_staff", "activo")
    search_fields = ("email", "nombre_completo")
    ordering = ("email",)