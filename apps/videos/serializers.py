from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from videos.models import Video
from viewers.models import Viewer


class VideoListSerializer(serializers.ModelSerializer):
    """
    List of a channel's videos.
    """
    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = [
            "title",
            "thumbnail",
            "token",
            "channel",
            "date",
            "user",
            "is_published"
        ]


class VideoCreateSerializer(serializers.ModelSerializer):
    """
    Create a new video
    """
    class Meta:
        model = Video
        fields = [
            "title",
            "description",
            "file",
            "thumbnail",
            "allow_comment",
            "visibility",
            "date",
            "token"
        ]

        read_only_fields = [
            'token',
            'date',
        ]
    
    def save(self, **kwargs):
        kwargs.setdefault('user', self.context['user'])
        kwargs.setdefault('channel', self.context['channel'])

        try:
            return super().save(**kwargs)
    
        except PermissionDenied as error:
            raise serializers.ValidationError(str(error))


class VideoDetailSerializer(serializers.ModelSerializer):
    '''Serializer for retrieving, Updating a video'''

    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    get_viewer_count = serializers.SerializerMethodField(
        method_name="get_viewer_count",
        read_only=True
    )

    class Meta:
        model = Video
        fields = [
            "title", 
            "description", 
            "file", 
            "thumbnail", 
            "token", 
            "user", 
            "channel", 
            "date", 
            "get_visibility_display",
            "visibility", 
            "is_updated", 
            "is_published", 
            "allow_comment", 
            "get_viewer_count"
            ]

        extra_kwargs = {
            "file" : {'read_only' : True},
            "token" : {'read_only' : True},
            "user" : {'read_only' : True},
            "channel" : {'read_only' : True},
            "date" : {'read_only' : True},
            "is_updated" : {'read_only' : True},
        }

    def get_viewer_count(self, obj):
        """
        Get the number of viewers for a video
        """
        return Viewer.objects.get_count(
            content_type=obj.get_content_type,
            channel=obj.channel,
        )
