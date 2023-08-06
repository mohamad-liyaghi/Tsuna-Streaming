from django.urls import path, include
from channels.views import ChannelListCreateView, ChannelDetailView


app_name = "channels"

V1 = [
    path(
        '',
        ChannelListCreateView.as_view(),
        name='list-create'
    ),
    path(
        '<str:channel_token>/',
        ChannelDetailView.as_view(),
        name='channel_detail'
    ),
]

urlpatterns = [
    path('v1/', include(V1)),
]
