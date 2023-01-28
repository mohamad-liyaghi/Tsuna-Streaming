from rest_framework import serializers
from videos.models import Video
from channels.models import Channel, ChannelAdmin

class VideoListSerializer(serializers.ModelSerializer):
    '''A serializer for user latest videos list'''
    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = ["title", "thumbnail", "token", "channel", "date", "user", "is_published"]


class CustomSlugRelatedField(serializers.SlugRelatedField):
    '''Get channels that user owns or they are admin and can add video'''
    def get_queryset(self):
        user = self.context.get("user")
        user_admin = ChannelAdmin.objects.filter(user=user, add_video=True).values("channel__id")
        channel_admin = Channel.objects.filter(id__in=user_admin)
        return Channel.objects.filter(owner=user) | channel_admin


class VideoCreateSeriaizer(serializers.ModelSerializer):
    '''Serializer for adding new video'''

    # get queryset custom for foreign key
    channel = CustomSlugRelatedField(queryset=Channel.objects.all(), slug_field='title')

    class Meta:
        model = Video
        fields = ["title", "description", "video", "thumbnail", "channel", "visibility", "date", "token"]

        extra_kwargs = {
            "date" : {'read_only' : True},
            "token" : {'read_only' : True}
        }
    
    def save(self, **kwargs):
        # set user for video uploader
        kwargs["user"] = self.context['user']
        return super().save(**kwargs)


class VideoDetailSerializer(serializers.ModelSerializer):
    '''Serializer for retrieving, Updating a video'''

    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = [ "title", "description", "video", "thumbnail", "token", "user", 
                        "channel", "date", "get_visibility_display", "visibility", "is_updated", "is_published"]

        extra_kwargs = {
            "video" : {'read_only' : True},
            "token" : {'read_only' : True},
            "user" : {'read_only' : True},
            "channel" : {'read_only' : True},
            "date" : {'read_only' : True},
            "is_updated" : {'read_only' : True},
        }