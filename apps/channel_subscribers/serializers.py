from rest_framework import serializers
from channel_subscribers.models import ChannelSubscriber

class SubscriberListSerializer(serializers.Serializer):
    user = serializers.CharField()
    date = serializers.DateTimeField()