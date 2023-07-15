from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from videos.models import Video


class VideoListSerializer(serializers.ModelSerializer):
    '''A serializer for user latest videos list'''
    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = ["title", "thumbnail", "token", "channel", "date", "user", "is_published"]


class VideoCreateSeriaizer(serializers.ModelSerializer):
    '''Serializer for adding new video'''


    class Meta:
        model = Video
        fields = ["title", "description", "file", "thumbnail", "allow_comment", "visibility", "date", "token"]

        extra_kwargs = {
            "date" : {'read_only' : True},
            "token" : {'read_only' : True}
        }
    
    def save(self, **kwargs):
        # set user for video uploader
        kwargs["user"] = self.context['user']
        kwargs["channel"] = self.context['channel']

        try:
            return super().save(**kwargs)
    
        except PermissionDenied as error:
            raise serializers.ValidationError(str(error))


class VideoDetailSerializer(serializers.ModelSerializer):
    '''Serializer for retrieving, Updating a video'''

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
            # "get_viewer_count" #TOOD: make this work
            ]

        extra_kwargs = {
            "file" : {'read_only' : True},
            "token" : {'read_only' : True},
            "user" : {'read_only' : True},
            "channel" : {'read_only' : True},
            "date" : {'read_only' : True},
            "is_updated" : {'read_only' : True},
        }
