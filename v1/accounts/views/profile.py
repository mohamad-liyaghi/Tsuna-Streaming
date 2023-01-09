from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from accounts.serializers.profile import ProfileSerializer


USER = get_user_model()


class ProfileView(RetrieveUpdateAPIView):
    '''
        A viewset for retrieving and updating a profile
    '''
    serializer_class = ProfileSerializer
    

    def get_object(self):
        return get_object_or_404(USER, user_id=self.kwargs["user_id"])
    

    def get(self, request, *args, **kwargs):
        '''Return given users information'''
        return super().get(request, *args, **kwargs)
