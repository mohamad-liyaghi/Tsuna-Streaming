from rest_framework import serializers
from videos.models import Video

class VideoListSerializer(serializers.ModelSerializer):
    '''A serializer for user latest videos list'''
    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = ["title", "thumbnail", "token", "channel", "date", "user", "is_published"]