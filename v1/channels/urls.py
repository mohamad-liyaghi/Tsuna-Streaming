from django.urls import path
from rest_framework import routers
from channels.views.channel import ChannelViewSet

app_name = "v1_channels"
router = routers.DefaultRouter()

router.register("channel", ChannelViewSet, basename="channel")

urlpatterns = []

urlpatterns += router.urls