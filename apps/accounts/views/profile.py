from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from accounts.serializers import ProfileSerializer
from accounts.permissions import CanUpdateProfile

USER = get_user_model()


@extend_schema_view(
    get=extend_schema(
        description='''Retrieve a Users public profile page.''',
        responses={
            200: 'ok',
            404: 'Not Found',
        }
    ),
    put=extend_schema(
        description='''Update users profile page (by its owner).''',
        responses={
            200: 'ok',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
        }
    ),
    patch=extend_schema(
        description='''Update users profile page (by its owner).'''
    ),
)
class ProfileView(RetrieveUpdateAPIView):
    """
    Retrieve/Update/ a Users public profile page.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, CanUpdateProfile]

    def get_object(self):
        profile = get_object_or_404(
            USER,
            token=self.kwargs["user_token"],
            is_active=True,
        )
        # Check permission for updating data
        self.check_object_permissions(self.request, profile)
        return profile
