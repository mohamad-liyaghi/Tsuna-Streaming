from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    '''Only allow admins to access a page'''
    message = 'Only admins can perform this action'

    def has_permission(self, request, view):
        return (request.user.is_admi())
    

class IsNormalUser(BasePermission):
    '''Only allow normal users to access the page'''

    message = 'You are already a premium user'

    def has_permission(self, request, view):
        return (request.user.is_normal())