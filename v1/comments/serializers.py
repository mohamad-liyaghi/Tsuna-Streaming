from rest_framework import serializers
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ["user", "body", "date", "edited", "pinned", "token"]
        extra_kwargs = {
            "edited" : {"read_only" : True},
            "pinned" : {"read_only" : True},
            "token" : {"read_only" : True},
        }