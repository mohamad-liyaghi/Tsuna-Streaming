from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from accounts.models import Plan
from accounts.permissions import AllowAdminPermission, AllowAuthenticatedPermission
from accounts.serializers.subscription import PlanListSerializer, PlanDetailSerializer, AvailabilitySerializer

@extend_schema_view(
    list=extend_schema(
        description="List of subscription plans."
    ),
    create=extend_schema(
        description="Create a new subscription plan [Admin only]."
    ),
    retrieve=extend_schema(
        description="Detail page of a subscription plan."
    ),
    update=extend_schema(
        description="Update a subscription plan [Admin only]."
    ),
    partial_update=extend_schema(
        description="Update a subscription plan [Admin only]."
    ),
    destroy=extend_schema(
        description="Delete a subscription plan [Admin only]."
    ),
    availability=extend_schema(
        description="Change is_available status of a subscription plan [Admin only]."
    ),
)
class SubscriptionViewSet(ModelViewSet):
    '''A Viewset for Creating, retrieving, updating and deleting plans and buy subscriptions.'''
    queryset = Plan.objects.all().order_by("-is_available", "active_months")
    lookup_field = "token"

    def get_serializer_class(self):
        '''Return the appropriate serializer'''

        if self.action in ["list", "create"]:
            return PlanListSerializer

        elif self.action in ["retrieve", "update", "partial_update"]:
            return PlanDetailSerializer
        
        elif self.action == "availability":
            return AvailabilitySerializer
    
    def get_permissions(self):
        '''return the appropriate permission class'''

        if self.action in ["list", "retrieve", "availability"] and self.request.method == "GET":
            permission_classes = [AllowAuthenticatedPermission]

        else:
            permission_classes = [AllowAdminPermission]

        return [permission() for permission in permission_classes]
    
    def destroy(self, request, *args, **kwargs):
        #TODO Check that nobody is using the plan
        return super().destroy(request, *args, **kwargs)
    
    
    @action(detail=True, methods=["GET", "POST"], url_path="availability")
    def availability(self, request, token):
    
        if request.method == "GET":
            object = self.get_object()
            return Response("{}'s availability is set to {}".format(object.title, object.is_available))
        
        elif request.method == "POST":
            object = self.get_object()
            if object.is_available:
                object.is_available = False
                object.save()
                return Response("{}'s availability is set to {}".format(object.title, object.is_available))

            object.is_available = True
            object.save()
            return Response("{}'s availability is set to {}".format(object.title, object.is_available))

    
        