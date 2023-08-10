from rest_framework import serializers
from contents.models import AbstractContent
from core.utils import get_content_type_model
from viewers.models import Viewer


class ContentDetailMethodSerializer(serializers.Serializer):
    """
    Provide necessary fields for content detail serializers.
    """
    content_type_id = serializers.SerializerMethodField(
        method_name='get_content_type_id',
        read_only=True
    )
    viewers_count = serializers.SerializerMethodField(
        method_name='get_viewers_count',
        read_only=True
    )

    def get_content_type_id(self, obj: AbstractContent) -> int:
        """
        Return content type id for a content object.
        """
        return get_content_type_model(model=type(obj)).id

    def get_viewers_count(self, obj) -> int:
        """
        Return Viewer count for a content object.
        """
        return Viewer.objects.get_count(
            content_object=obj,
            channel=obj.channel,
        )