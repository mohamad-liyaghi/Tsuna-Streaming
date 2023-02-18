from django.urls import path
from rest_framework import routers
from channels.views.channel import ChannelViewSet
from channels.views.admin import ChannelAdminView, ChannelAdminDetailView
from channels.views.subscriber import SubscriberView, SubscriberBlockView, SubscriberListView, SubscribedChannelListView

app_name = "v1_channels"
router = routers.DefaultRouter()

router.register("channel", ChannelViewSet, basename="channel")

urlpatterns = [
    # channel admin endpoints
    path("channel/<str:token>/admin/", ChannelAdminView.as_view(), name="channel_admin"),
    path("channel/<str:channel_token>/admin/<str:admin_token>/", ChannelAdminDetailView.as_view(), name="channel_admin_detail"),

    # subscriber endpoints
    path("channel/subscribed/", SubscribedChannelListView.as_view(), name='subscribed_channels'),
    path("channel/<str:channel_token>/subscriber/", SubscriberView.as_view(), name="subscriber"),
    path("channel/<str:channel_token>/subscriber/block/<str:token>/", SubscriberBlockView.as_view(), name="block_subscriber"),
    path("channel/<str:channel_token>/subscriber/list", SubscriberListView.as_view(), name="subscriber_list"),
    path("channel/<str:channel_token>/subscriber/list/blocked/", SubscriberListView.as_view(), name="blocked_subscriber_list"),
    
]

urlpatterns += router.urls