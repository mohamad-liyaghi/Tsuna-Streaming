from rest_framework.permissions import BasePermission
from channel_subscribers.models import ChannelSubscriber


class CanSubscribePermission(BasePermission):
    """
    Permission to check if the user is already subscribed to the channel.
    """

    message = "You are already subscribed to this channel."

    def has_object_permission(self, request, view, obj):
        subscribed = ChannelSubscriber.objects.get_from_cache(
            user=request.user, channel=obj
        )
        return not bool(subscribed)


class CanUnSubscribePermission(BasePermission):
    """
    Permission to see if user subscribed a channel of not
    """

    message = "You havnt subscribed yet."

    def has_object_permission(self, request, view, obj):
        subscribed = ChannelSubscriber.objects.get_from_cache(
            user=request.user, channel=obj
        )
        return bool(subscribed)
