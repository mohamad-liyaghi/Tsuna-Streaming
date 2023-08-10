from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from videos.models import Video
from contents.serializers import ContentDetailMethodSerializer


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


class VideoDetailSerializer(
    serializers.ModelSerializer,
    ContentDetailMethodSerializer
):
    """
    A serializer for video detail and updating.
    """

    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

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
            "viewers_count",
            "content_type_id",
            ]

        read_only_fields = fields
