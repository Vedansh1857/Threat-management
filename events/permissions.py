from rest_framework.permissions import BasePermission

class IsAdminOnly(BasePermission):
    def has_permission(self, request):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        # Only Admins can access
        return user.groups.filter(name="Admin").exists()

