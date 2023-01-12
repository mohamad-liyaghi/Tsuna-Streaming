from rest_framework.viewsets import ModelViewSet
from accounts.models import Plan
from accounts.permissions import AllowAdminPermission, AllowAuthenticatedPermission
from accounts.serializers.subscription import PlanListSerializer


class SubscriptionViewSet(ModelViewSet):
    '''A Viewset for Creating, retrieving, updating and deleting plans and buy subscriptions.'''
    queryset = Plan.objects.all().order_by("-is_avaiable", "active_months")
    
    def get_serializer_class(self):
        '''Return the appropriate serializer'''

        if self.action in ["list", "create"]:
            return PlanListSerializer
    
    def get_permissions(self):
        '''return the appropriate permission class'''

        if self.action in ["list"]:
            permission_classes = [AllowAuthenticatedPermission]

        else:
            permission_classes = [AllowAdminPermission]

        return [permission() for permission in permission_classes]
        