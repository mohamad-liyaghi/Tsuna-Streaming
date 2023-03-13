from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from memberships.serializers.membership import MembershipSerializer
from memberships.models import Membership
from memberships.permissions import IsAdminUser


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
