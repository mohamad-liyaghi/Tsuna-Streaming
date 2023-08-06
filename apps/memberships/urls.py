from django.urls import path, include
from memberships.views import (
    MembershipListCreateView, 
    MembershipDetailView, 
    MembershipSubscribeView
)

app_name = 'memberships'

V1 = [
    path("", MembershipListCreateView.as_view(), name='membership'),
    path(
        "<str:membership_token>/",
        MembershipDetailView.as_view(),
        name='membership_detail'
    ),
    path(
        "<str:membership_token>/subscribe/",
        MembershipSubscribeView.as_view(),
        name='membership_subscribe'
    ),
]

urlpatterns = [
    path("v1/", include(V1)),
]
