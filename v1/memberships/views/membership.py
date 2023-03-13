from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from memberships.models import Membership
from memberships.permissions import IsAdminUser
from memberships.serializers.membership import (
    MembershipSerializer,
    MembershipDetailSerializer
)


@extend_schema_view(
    list=extend_schema(
        description="List of all Memberships."
    ),
    create=extend_schema(
        description="Create a new Membership Plan [Admin only]."
    ),
)
class MembershipListCreateView(ListCreateAPIView):
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminUser()]
        
        else:
            return [IsAuthenticated(),]
    
    @method_decorator(cache_page(60 * 5))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



@extend_schema_view(
    retrieve=extend_schema(
        description="Detail page of a Membership."
    ),
    update=extend_schema(
        description="Update a Membership Plan [Admin only]."
    ),
    destroy=extend_schema(
        description="Delete a new Membership Plan [Admin only]."
    ),
)
class MembershipDetailAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = MembershipDetailSerializer

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        # Only admins can update/Delete a plan
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdminUser()]
        
        else:
            return [IsAuthenticated(),]

    def get_object(self):
        return get_object_or_404(Membership, token=self.kwargs['membership_token'])
    

    def destroy(self, request, *args, **kwargs):
        
        try:
            return super().destroy(request, *args, **kwargs)
        
        # return error message if sth goes wrong
        except ValidationError as error:
            return Response(str(error), status=status.HTTP_403_FORBIDDEN)
