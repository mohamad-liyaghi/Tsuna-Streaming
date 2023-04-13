from django.urls import path
from channels.views import ChannelListCreateView, ChannelDetailView


app_name = "v1_channels"

urlpatterns = [
    path('', ChannelListCreateView.as_view(), name='channel_list_create'),
    path('<str:channel_token>/', ChannelDetailView.as_view(), name='channel_detail'),
]

