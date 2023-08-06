from rest_framework import serializers
from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber
from channels.exceptions import ChannelLimitExceededException


class ChannelListCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and creating channels.
    """

    class Meta:
        model = Channel
        fields = [
            "title",
            "description",
            "avatar",
            "thumbnail", 
            "token",
            "date_created",
            "is_verified"
            ]

        read_only_fields = [
            "token",
            "date_created",
            "is_verified"
            ]
        write_only_fields = [
            "description",
            "avatar",
        ]

    def create(self, validated_data):
        """
        Create a new channel.
        """
        try:
            return Channel.objects.create(
                owner=self.context["request"].user,
                **validated_data
            )
        except ChannelLimitExceededException as error:
            raise serializers.ValidationError(str(error))


class ChannelDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    role = serializers.SerializerMethodField(
        method_name="role_in_channel"
    )
    subscribers_count = serializers.SerializerMethodField(
        method_name='get_subscriber_count'
    )

    class Meta:
        model = Channel
        fields = [
            "title",
            "description", 
            "avatar",
            "thumbnail",
            "owner", 
            "token", 
            "date_created",
            "is_verified", 
            "role", 
            "subscribers_count",
            ]

        read_only_fields = [
            'token',
            'owner',
            'date_created',
            'is_verified',
            'role',
        ]

    def role_in_channel(self, channel):
        """
        Return user role in channel.
        We have 2 roles in channel:
            1. Owner
            2. Admin
        """
        user = self.context['request'].user

        if channel.owner == user:
            return "owner"

        if user.channel_admins.filter(channel=channel).exists():
            return "Admin"

        return

    def get_subscriber_count(self, channel) -> int:
        """
        Return number of a channel subscribers
        """
        return ChannelSubscriber.objects.get_count(channel=channel)
