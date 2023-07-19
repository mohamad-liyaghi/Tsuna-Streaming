from django.shortcuts import get_object_or_404
from memberships.exceptions import MembershipInUserError

from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView, 
    CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from memberships.models import Membership
from memberships.permissions import IsAdmin, CanSubscribeMembership
from memberships.serializers import (
    MembershipSerializer,
    MembershipDetailSerializer, 
    MembershipSubscribeSerializer
)


@extend_schema_view(
    get=extend_schema(
        description="List of all Membership Plans.",
        responses={
            200: 'Ok',
            401: 'Unauthorized',
        },
        tags=['Memberships']
    ),
    post=extend_schema(
        description="Create a new Membership Plan [Admin only].",
        responses={
            201: 'Created',
            401: 'Unauthorized',
            403: 'Forbidden',
        },
        tags=['Memberships']
    ),
)
class MembershipListCreateView(ListCreateAPIView):
    """
    List all Membership Plans or Create a new Membership Plan.
    Methods: GET, POST
    """
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()
    
    def get_permissions(self):
        if self.request.method == "POST":
            # Only admins can create a plan
            return [IsAuthenticated(), IsAdmin()]
        else:
            return [IsAuthenticated()]
    

@extend_schema_view(
    get=extend_schema(
        description="Detail page of a Membership plan.",
        responses={
            200: 'Ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
        },
        tags=['Memberships']
    ),
    put=extend_schema(
        description="Update a Membership Plan [Admin only].",
        responses={
            200: 'Ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
        },
        tags=['Memberships']
    ),
    patch=extend_schema(
        description="Update a Membership Plan [Admin only].",
        responses={
            200: 'Ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
        },
        tags=['Memberships']
    ),
    delete=extend_schema(
        description="Delete a new Membership Plan [Admin only].",
        responses={
            204: 'No Content',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
        },
        tags=['Memberships']
    ),
)
class MembershipDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or Delete a Membership Plan.
    Methods: GET, PUT, PATCH, DELETE
    """
    serializer_class = MembershipDetailSerializer

    def get_permissions(self):
        # Only admins can update/Delete a plan
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdmin()]
        
        else:
            return [IsAuthenticated()]

    def get_object(self):
        return get_object_or_404(
            Membership,
            token=self.kwargs['membership_token']
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Membership Plan.
        If raised MembershipInUserError, return error message.
        """
        try:
            return super().destroy(request, *args, **kwargs)

        except MembershipInUserError as error:
            # Return error message if raised MembershipInUserError
            return Response(
                str(error), status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(
    create=extend_schema(
        description="Subscribe to a membership plan [Normal users only]."
    ),
)
class MembershipSubscribeView(CreateAPIView):
    '''Create Subscription for user (Subscribe to a membership plan)'''

    permission_classes = [IsAuthenticated, CanSubscribeMembership]
    serializer_class  = MembershipSubscribeSerializer
    
    def get_object(self):
        return get_object_or_404(Membership, token=self.kwargs['membership_token'])
    
    def get_serializer_context(self):
        return {"membership" : self.get_object(), 'user' : self.request.user}
    
