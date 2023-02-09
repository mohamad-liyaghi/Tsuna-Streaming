from rest_framework.permissions import BasePermission


class AllowUnAuthenticatedPermission(BasePermission):
    '''Access unauthorised users'''

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class AllowAdminPermission(BasePermission):
    '''Only allow admins to access a page'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "a"