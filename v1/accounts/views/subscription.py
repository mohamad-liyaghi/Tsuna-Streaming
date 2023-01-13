from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import Plan
from accounts.permissions import AllowAdminPermission, AllowAuthenticatedPermission
from accounts.serializers.subscription import PlanListSerializer, PlanDetailSerializer, AvailabilitySerializer


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

    
        