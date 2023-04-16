from django.urls import path
from .views import (
    AdminListCreateView,
    AdminDetailView,
    AdminPermissionDetail,
)

app_name = 'v1_admins'

urlpatterns = [
    path('<str:channel_token>/', AdminListCreateView.as_view(), name='admin_list_create'),
    path('<str:channel_token>/<str:admin_token>/', AdminDetailView.as_view(), name='admin_detail'),
    path(
            '<str:channel_token>/<str:admin_token>/<str:permission_token>',
            AdminPermissionDetail.as_view(),
            name='admin_permission_detail'
    ),
]
