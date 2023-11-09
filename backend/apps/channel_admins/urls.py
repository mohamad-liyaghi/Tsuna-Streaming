from django.urls import path, include
from .views import (
    AdminListCreateView,
    AdminDetailView,
)

app_name = "channel_admins"

V1 = [
    path(
        "<str:channel_token>/", AdminListCreateView.as_view(), name="admin_list_create"
    ),
    path(
        "<str:channel_token>/<str:admin_token>/",
        AdminDetailView.as_view(),
        name="admin_detail",
    ),
]

urlpatterns = [
    path("v1/", include(V1)),
]
