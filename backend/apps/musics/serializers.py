from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from musics.models import Music
from contents.serializers import ContentDetailMethodSerializer


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
            "is_published",
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
            "token",
        ]

        read_only_fields = [
            "token",
            "date",
        ]

    def save(self, **kwargs):
        kwargs.setdefault("user", self.context["user"])
        kwargs.setdefault("channel", self.context["channel"])

        try:
            return super().save(**kwargs)

        except PermissionDenied as error:
            raise serializers.ValidationError(str(error))


class MusicDetailSerializer(ContentDetailMethodSerializer, serializers.ModelSerializer):
    """
    A serializer for music detail.
    """

    channel = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

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
            "viewers_count",
            "content_type_id",  # From BaseContentSerializer
        ]

        read_only_fields = fields
