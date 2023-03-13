from django.urls import path
from memberships.views.membership import MembershipListCreateView

app_name = 'v1_memberships'

urlpatterns = [
    path("membership/", MembershipListCreateView.as_view(), name='membership'),
]
