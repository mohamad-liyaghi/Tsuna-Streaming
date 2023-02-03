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


class CommentRepliesSerializer(serializers.Serializer):
    user = serializers.CharField()
    body = serializers.CharField()
    token = serializers.CharField()


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField(method_name="reply_list")

    class Meta:
        model = Comment
        fields = ["user", "body", "date", "edited", "pinned", "token", "replies"]

    def reply_list(self, comment):
        serializer = CommentRepliesSerializer(instance=comment.replies.all(), many=True)
        return serializer.data