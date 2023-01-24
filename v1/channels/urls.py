from django.urls import path
from rest_framework import routers
from channels.views.channel import ChannelViewSet
from channels.views.admin import ChannelAdminView, ChannelAdminDetailView
from channels.views.subscriber import SubscriberView, SubscriberBlockView

app_name = "v1_channels"
router = routers.DefaultRouter()

router.register("channel", ChannelViewSet, basename="channel")

urlpatterns = [
    path("channel-admin/<str:token>/", ChannelAdminView.as_view(), name="channel_admin"),
    path("channel-admin/<str:channel_token>/<str:admin_token>/", ChannelAdminDetailView.as_view(), name="channel_admin_detail"),

    path("subscriber/<str:channel_token>/", SubscriberView.as_view(), name="subscriber"),
    path("subscriber/<str:channel_token>/block/<str:user_id>/", SubscriberBlockView.as_view(), name="block_subscriber"),
    
]

urlpatterns += router.urls