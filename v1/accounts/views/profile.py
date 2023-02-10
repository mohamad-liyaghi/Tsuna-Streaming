from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status

from drf_spectacular.utils import extend_schema, extend_schema_view

from accounts.serializers.profile import ProfileSerializer
from rest_framework.response import Response

USER = get_user_model()

@extend_schema_view(
    get=extend_schema(
        description='''Given Users public profile page.'''
    ),
    put=extend_schema(
        description='''Update users public profile page.'''
    ),
    patch=extend_schema(
        description='''Update users public profile page.'''
    ),
)
class ProfileView(RetrieveUpdateAPIView):
    '''
        A viewset for retrieving and updating a profile
    '''
    serializer_class = ProfileSerializer
    

    def get_object(self):
        return get_object_or_404(USER, user_id=self.kwargs["user_id"])
    
    @method_decorator(cache_page(5))
    def get(self, request, *args, **kwargs):
        '''Return given users information'''
        return super().get(request, *args, **kwargs)
    
    
    def put(self, request, *args, **kwargs):
        '''Update a user (only the profile owner can update)'''
        if request.user ==  self.get_object():
            return super().put(request, *args, **kwargs)

        return Response("You can not update this page.", 
                        status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, *args, **kwargs):
        '''Update a user (only the profile owner can update)'''
        if request.user ==  self.get_object():
            return super().patch(request, *args, **kwargs)

        return Response("You can not update this page.", 
                        status=status.HTTP_403_FORBIDDEN)