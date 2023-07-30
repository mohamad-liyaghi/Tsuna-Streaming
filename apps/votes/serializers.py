from rest_framework import serializers
from votes.models import Vote


class VoteStatusSerializer(serializers.ModelSerializer):
    """
    Show a users vote status
    """
    class Meta:
        model = Vote
        fields = ["date", "choice"]


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["choice"]

    def create(self, validated_data):
        content_object = self.context['content_object']()
        user = self.context['user']

        return Vote.objects.create_in_cache(
            channel=content_object.channel,
            user=user,
            content_object=content_object,
            **validated_data
        )


class VoteListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Vote
        fields = ["user", "choice"]