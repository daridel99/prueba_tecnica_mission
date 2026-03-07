from rest_framework.permissions import BasePermission


class IsAdminOrOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.user.rol == "ADMIN":
            return True

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        if request.user.rol == "ANALISTA":
            return True

        return False


    def has_object_permission(self, request, view, obj):

        if request.user.rol == "ADMIN":
            return True

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        if request.user.rol == "ANALISTA":
            return obj.usuario == request.user

        return False