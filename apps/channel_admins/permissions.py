from rest_framework.permissions import BasePermission


class IsChannelOwner(BasePermission):
    """
    Check if user is the channel owner
    """

    message = 'You are not the owner of the channel.'

    def has_permission(self, request, view):
        """
        Check if the user is the owner of the channel.
        The view.channel is provided by the `ChannelMixin` for the view
        """
        return request.user == view.channel.owner


class AdminDetailPermission(BasePermission):
    '''Update admin prmission.'''

    message = 'You can not perform this action to this admin.'

    def has_permission(self, request, view):
        object = view.get_object()

        if request.method in ["PUT", "PATCh", "DELETE"]:
            return (request.user in [object.promoted_by, object.channel.owner])

        # if request.method is GET only the admins (check in mixin) can access the page.
        return True


class AdminPermissionUpdate(BasePermission):
    '''Update admin permissions prmission.'''

    message = 'You can not perform this action to this admin.'

    def has_permission(self, request, view):
        object = view.get_object()

        if request.method in ["PUT", "PATCh"]:
            return (request.user in [object.admin.promoted_by, object.admin.channel.owner])

        return True
