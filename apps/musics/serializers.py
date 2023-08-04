from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from musics.models import Music
from viewers.models import Viewer


class MusicListSerializer(serializers.ModelSerializer):
    """
    A serializer for channels latest musics list.
    """

    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Music
        fields = [
            "title",
            "thumbnail",
            "token",
            "channel",
            "date",
            "user",
            "is_published"
        ]


class MusicCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding new music.
    """

    class Meta:
        model = Music
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



class MusicDetailSerializer(serializers.ModelSerializer):
    '''Serializer for retrieving, Updating a music'''

    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    get_viewer_count = serializers.SerializerMethodField(
        method_name="get_viewer_count",
        read_only=True
    )

    class Meta:
        model = Music
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
            Return the number of viewers for a music.
            """
            return Viewer.objects.get_count(
                channel=obj.channel,
                content_object=obj
            )
