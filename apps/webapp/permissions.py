from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request):
        return True  # Разрешаем доступ к представлению

    def has_object_permission(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Разрешаем безопасные методы (GET, HEAD, OPTIONS)
        
        return obj.author == request.user 