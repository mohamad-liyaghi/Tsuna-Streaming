from rest_framework.permissions import BasePermission


class AllowUnAuthenticatedPermission(BasePermission):
    '''Access unauthorised users'''

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class ProfilePermission(BasePermission):
    '''A permission for updating profile that prevents updating others profile'''
    message = "You can only update your own profile."

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            return  (obj == request.user) 
        return True
    
            
    