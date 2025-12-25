from rest_framework.permissions import BasePermission, SAFE_METHODS

class AdminOrAnalystReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Must be logged in
        if not user or not user.is_authenticated:
            return False

        # Superuser always allowed
        if user.is_superuser:
            return True

        # Analysts & Admins can read
        if request.method in SAFE_METHODS:
            return user.groups.filter(name__in=["Admin", "Analyst"]).exists()

        # Only Admins can write
        return user.groups.filter(name="Admin").exists()
