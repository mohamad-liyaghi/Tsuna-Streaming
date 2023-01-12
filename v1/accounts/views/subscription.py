from rest_framework.viewsets import ModelViewSet
from accounts.models import Plan
from accounts.permissions import AllowAdminPermission, AllowAuthenticatedPermission

class SubscriptionViewSet(ModelViewSet):
    '''A Viewset for Creating, retrieving, updating and deleting plans and buy subscriptions.'''
    permission_classes = [AllowAdminPermission,]
    queryset = Plan.objects.all()