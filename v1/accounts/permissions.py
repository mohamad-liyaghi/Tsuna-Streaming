from rest_framework.permissions import BasePermission


class AllowUnAuthenticatedPermission(BasePermission):
    '''Access unauthorised users'''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False

        return True


class AllowAdminPermission(BasePermission):
    '''Only allow admins to access a page'''

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "a":
            return True

        return False

class AllowAuthenticatedPermission(BasePermission):
    '''Allow authenticated users'''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        return False