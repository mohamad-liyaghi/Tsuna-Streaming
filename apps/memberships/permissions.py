from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Only Allow Admins to perform this action.
    """
    message = 'Only admins can perform this action'

    def has_permission(self, request, view):
        return request.user.is_admin()
    

class CanSubscribeMembership(BasePermission):
    """
    Only allow normal users to subscribe to a membership plan.
    """
    message = 'Only normal users can perform this action'

    def has_permission(self, request, view):
        user = request.user
        return not user.is_admin() and not user.is_premium()
