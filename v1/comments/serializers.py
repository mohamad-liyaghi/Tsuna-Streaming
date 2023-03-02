from rest_framework import serializers
from comments.models import Comment
from comments.exceptions import CommentNotAllowed


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
    

    def save(self, **kwargs):
        try:
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