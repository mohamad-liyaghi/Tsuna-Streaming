from rest_framework import serializers
from comments.models import Comment
from comments.exceptions import CommentNotAllowed


class CommentParentQueryset(serializers.SlugRelatedField):
    '''List of object comments that can be replied.'''

    def get_queryset(self):
        # get the object that is sent from serializer
        object = self.context.get('object', None)
        # return comments of an object
        return object.comment.filter(parent__isnull=True)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    parent = CommentParentQueryset(slug_field='token', required=False)

    class Meta:
        model = Comment
        fields = ["parent", "user", "body", "date", "edited", "pinned", "token"]
        extra_kwargs = {
            "edited" : {"read_only" : True},
            "pinned" : {"read_only" : True},
            "token" : {"read_only" : True},
        }
    

    def save(self, **kwargs):
        try:
            kwargs.setdefault('user', self.context['user'])
            kwargs.setdefault('content_object', self.context['object'])
            return super().save(**kwargs)
        
        # user cannot add comment when comments are closed
        except CommentNotAllowed:
            raise serializers.ValidationError("Comments are not allowed.")


class CommentRepliesSerializer(serializers.Serializer):
    user = serializers.CharField()
    body = serializers.CharField()
    token = serializers.CharField()


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField(method_name="reply_list")
    vote_count = serializers.SerializerMethodField(method_name="vote_counts")

    class Meta:
        model = Comment
        fields = ["user", "body", "date", "edited", "pinned", "token", "vote_count", "replies"]
        extra_kwargs = {
            "edited" : {"read_only" : True},
            "pinned" : {"read_only" : True},
            "token" : {"read_only" : True},
        }


    def reply_list(self, comment):
        '''return list of comment list'''
        serializer = CommentRepliesSerializer(instance=comment.replies.all(), many=True)
        return serializer.data
    

    def vote_counts(self, comment):
        '''return count of vote of a comment''' 
        return {"upvotes" : comment.vote.upvotes(), "downvotes" : comment.vote.downvotes()}