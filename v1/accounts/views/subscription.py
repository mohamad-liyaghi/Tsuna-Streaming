from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, extend_schema_view

from accounts.models import Plan, Subscription
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
        
        elif self.action == "buy_plan":
            return AvailabilitySerializer
    
    def get_permissions(self):
        '''return the appropriate permission class'''

        if self.action in ["list", "retrieve", "availability", "buy_plan"] and self.request.method == "GET":
            permission_classes = [AllowAuthenticatedPermission]

        elif self.action in ["buy_plan"] and self.request.method == "POST":
            permission_classes = [AllowAuthenticatedPermission]

        else:
            permission_classes = [AllowAdminPermission]

        return [permission() for permission in permission_classes]
    
    def destroy(self, request, *args, **kwargs):
        '''Check if there is no subsription with given plan'''
        subscription = Subscription.objects.filter(plan=self.get_object())
        if subscription:
            return Response("You can not delete this plan. {} users are using this plan".format(subscription.count()))
            
        return super().destroy(request, *args, **kwargs)
    

    @method_decorator(cache_page(5))
    @action(detail=True, methods=["GET", "POST"], url_path="availability")
    def availability(self, request, token):
    
        if request.method == "GET":
            object = self.get_object()
            return Response("{}'s availability is set to {}".format(object.title, object.is_available),
            status=status.HTTP_200_OK)
        
        elif request.method == "POST":
            object = self.get_object()
            if object.is_available:
                object.is_available = False
                object.save()
                return Response("{}'s availability is set to {}".format(object.title, object.is_available),
                status=status.HTTP_200_OK)

            object.is_available = True
            object.save()
            return Response("{}'s availability is set to {}".format(object.title, object.is_available), 
            status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST", "GET"], url_path="buy")
    def buy_plan(self, request, token):
        if request.method == "GET":
            return Response("{} purchase page.".format(self.get_object().title))

        elif self.request.method == "POST":
            if not self.get_object().is_available:
                return Response("This item is not currently available")

            if request.user.role in ["a","p"]:
                return Response("You are already a premium user.")

            Subscription.objects.create(user=request.user, plan=self.get_object())
            return Response("You are now a premium user.", status=status.HTTP_200_OK)

    @method_decorator(cache_page(5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(5))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    
        