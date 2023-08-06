from rest_framework.permissions import BasePermission


class AllowUnAuthenticatedPermission(BasePermission):
    """
    Only allow unauthenticated users to access this view.
    """

    message = "Authenticated users are not allowed to access this view"

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class CanUpdateProfile(BasePermission):
    message = "Only profile owner can update this profile."

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            return obj == request.user
        return True
