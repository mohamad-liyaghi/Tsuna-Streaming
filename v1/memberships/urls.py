from django.urls import path
from memberships.views import (
    MembershipListCreateView, 
    MembershipDetailView, 
    MembershipSubscribeView
)


app_name = 'v1_memberships'

urlpatterns = [
    path("membership/", MembershipListCreateView.as_view(), name='membership'),
    path("membership/<str:membership_token>/", MembershipDetailView.as_view(), name='membership_detail'),
    path(
            "membership/<str:membership_token>/subscribe/",
            MembershipSubscribeView.as_view(),
            name='membership_detail'
        ),
]
