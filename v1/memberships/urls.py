from django.urls import path
from memberships.views.membership import MembershipListCreateView, MembershipDetailAPIView

app_name = 'v1_memberships'

urlpatterns = [
    path("membership/", MembershipListCreateView.as_view(), name='membership'),
    path("membership/<str:membership_token>/", MembershipDetailAPIView.as_view(), name='membership_detail'),
]
