from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "nombre_completo",
            "rol"
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            **validated_data
        )

        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "nombre_completo", "rol"]
        read_only_fields = ["id"]