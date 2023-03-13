from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    '''Only allow admins to access a page'''
    message = 'Only admins can perform this action'

    def has_permission(self, request, view):
        return (request.user.role == "a")