from rest_framework import serializers
from channels.models import Channel, ChannelAdmin


class ChannelListCreateSerializer(serializers.ModelSerializer):
    '''A serializer for listing and creating a Channel'''

    class Meta:
        model = Channel
        fields = [
            "title",
            "description",
            "profile",
            "thumbnail", 
            "token", 
            "date_joined", 
            "is_verified"
            ]

        extra_kwargs = {
            'token': {"read_only" : True},
            'date_joined': {"read_only" : True},
            'is_verified': {"read_only" : True},
            'date_joined': {"read_only" : True},
            'description': {"write_only" : True},
            'thumbnail': {"write_only" : True},
        }
    
    def create(self, validated_data):
        '''Set request.user as owner of a channel'''

        validated_data["owner"] = self.context["request"].user
        channel = super().create(validated_data)
        return channel



class ChannelDetailSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()
    role = serializers.SerializerMethodField(method_name="role_in_channel")
    subscribers = serializers.SerializerMethodField(method_name="subscriber_count")
    videos = serializers.SerializerMethodField(method_name="video_count")

    class Meta:
        model = Channel
        fields = ["title", "description", "profile", "thumbnail", 
                        "owner", "token", "date_joined", "is_verified", "role", "subscribers", "videos"]
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
    
    def subscriber_count(self, channel):
        return channel.subscribers.count()

    def video_count(self, channel):
        return channel.videos.filter(visibility="pu").count()