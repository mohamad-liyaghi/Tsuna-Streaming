from rest_framework import serializers
from comments.models import Comment
from comments.exceptions import CommentNotAllowed


class CommentParentQueryset(serializers.SlugRelatedField):
    """
    Return parent comment of a comment.
    """

    def get_queryset(self):
        # Content object is passed to serializer context in views.
        content_object = self.context['content_object']()
        # return parent comments of content object.
        return content_object.comments.filter(parent__isnull=True)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    parent = CommentParentQueryset(
        slug_field='token',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Comment
        fields = [
            "parent",
            "user",
            "body",
            "date",
            "edited",
            "pinned",
            "token"
        ]

        read_only_fields = [
            "date",
            "edited",
            "pinned",
            "token"
        ]

    def save(self, **kwargs):
        # Set User and Content Object
        kwargs.setdefault('user', self.context['user'])
        kwargs.setdefault('content_object', self.context['content_object']())
        try:
            return Comment.objects.create(**kwargs)

        # If comments are not allowed for content object,
        # raise CommentNotAllowed exception.
        except CommentNotAllowed:
            raise serializers.ValidationError(
                "Comments are not allowed for this object."
            )


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
        extra_kwargs = {
            "edited" : {"read_only" : True},
            "pinned" : {"read_only" : True},
            "token" : {"read_only" : True},
        }


    def reply_list(self, comment):
        '''return list of comment list'''
        serializer = CommentRepliesSerializer(instance=comment.replies.select_related('user').all(), many=True)
        return serializer.data