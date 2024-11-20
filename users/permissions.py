from rest_framework.permissions import BasePermission

class IsAuthenticatedUser(BasePermission):
    """
    Allow access only to authenticated users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsFarmer(BasePermission):
    """
    Allows access only to farmer users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer' or request.user.role == 'admin'

class IsBuyer(BasePermission):
    """
    Allows access only to buyer users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'buyer' or request.user.role == 'admin'