from django.urls import path
from memberships.views import (
    MembershipListCreateView, 
    MembershipDetailView, 
    MembershipSubscribeView
)


app_name = 'memberships'

urlpatterns = [
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
