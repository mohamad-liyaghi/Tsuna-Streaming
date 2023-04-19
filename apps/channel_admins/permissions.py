from rest_framework.permissions import BasePermission

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