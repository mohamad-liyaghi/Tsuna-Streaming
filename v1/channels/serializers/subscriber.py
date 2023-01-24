from rest_framework import serializers
from channels.models import ChannelSubscriber


class SubscriberListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = ChannelSubscriber
        fields = ["user", "date"]