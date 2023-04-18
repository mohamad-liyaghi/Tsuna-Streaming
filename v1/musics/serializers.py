from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from musics.models import Music


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


class MusicCreateSeriaizer(serializers.ModelSerializer):
    """
    Serializer for adding new music.
    """

    class Meta:
        model = Music
        fields = [
            "title",
            "description",
            "music",
            "thumbnail",
            "allow_comment",
            "visibility",
            "date",
            "token"
        ]
        extra_kwargs = {
            "date": {'read_only': True},
            "token": {'read_only': True}
        }

    def save(self, **kwargs):
        """
        Sets user for music uploader.
        """

        kwargs["user"] = self.context['user']
        kwargs["channel"] = self.context['channel']

        try:
            return super().save(**kwargs)

        except PermissionDenied as error:
            raise serializers.ValidationError(str(error))
