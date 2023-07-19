from rest_framework import serializers
from channels.models import Channel
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
    role = serializers.SerializerMethodField(method_name="role_in_channel")

    class Meta:
        model = Channel
        fields = [
            "title",
            "description", 
            "profile",
            "thumbnail", 
            "owner", 
            "token", 
            "date_joined",
            "is_verified", 
            "role", 
            # "subscribers_count",  # TODO : add subscribers count
            ]

        extra_kwargs = {
            "token" : {"read_only" : True},
            "owner" : {"read_only" : True},
            "is_verified" : {"read_only" : True},
            "role" : {"read_only" : True}
        }

    def role_in_channel(self, channel):
        '''Return the user role in channel'''
        user = self.context['request'].user

        if channel.owner == user:
            return "owner"

        if user.channel_admins.filter(channel=channel).exists():
            return "Admin"
            
        return None