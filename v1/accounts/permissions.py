from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    '''Access unauthorised users'''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False

        return True
