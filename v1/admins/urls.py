from django.urls import path
from .views import (
    AdminListCreateView,
    AdminDetailView,
)

app_name = 'v1_admins'

urlpatterns = [
    path('admin/<str:channel_token>/', AdminListCreateView.as_view(), name='admin_list_create'),
    path('admin/<str:channel_token>/<str:admin_token>/', AdminDetailView.as_view(), name='admin_detail'),
]
