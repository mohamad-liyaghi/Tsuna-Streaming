from rest_framework.permissions import BasePermission


class AllowUnAuthenticatedPermission(BasePermission):
    '''Access unauthorised users'''

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class AllowAdminPermission(BasePermission):
    '''Only allow admins to access a page'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "a"


class ProfilePermission(BasePermission):
    '''A permission for updating profile that prevents updating others profile'''
    message = "You can only update your own profile."

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            return  (obj == request.user) 
        return True
    

class AllowNonPremiumPermission(BasePermission):
    '''Allow only non premium users for buying premium plans.'''

    message = 'User is already a premium user.'

    def has_permission(self, request, view):
        return not (request.user.role in ["a", "p"])
            
    