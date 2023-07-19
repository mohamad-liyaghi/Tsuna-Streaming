from django.urls import path
from channels.views import ChannelListCreateView, ChannelDetailView


app_name = "channels"

urlpatterns = [
    path(
        '',
        ChannelListCreateView.as_view(),
        name='list-create'
    ),
    path('<str:channel_token>/', ChannelDetailView.as_view(), name='channel_detail'),
]

