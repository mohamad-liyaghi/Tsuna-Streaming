from rest_framework import serializers
from channels.models import Channel, ChannelAdmin


class ChannelListSerializer(serializers.ModelSerializer):
    # TODO get subs count
    # TODO Add user role in channel
    class Meta:
        model = Channel
        fields = ["profile", "title", "token", "is_verified"]


class ChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["title", "description", "profile", "thumbnail", "token", "date_joined"]
        extra_kwargs = {
            'token': {"read_only" : True},
            'date_joined': {"read_only" : True},
        }


    def create(self, validated_data):
        '''Set request.user as owner of a channel'''

        validated_data["owner"] = self.context["request"].user
        channel = super().create(validated_data)
        return channel


class ChannelDetailSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()
    role = serializers.SerializerMethodField(method_name="role_in_channel")

    class Meta:
        model = Channel
        fields = ["title", "description", "profile", "thumbnail", 
                        "owner", "token", "date_joined", "is_verified", "role"]
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

        if ChannelAdmin.objects.filter(channel=channel, user=user).exists():
            return "Admin"
            
        return None