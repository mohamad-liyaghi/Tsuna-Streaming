from rest_framework import serializers
from votes.models import Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["choice"]


class VoteListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Vote
        fields = ["user", "choice"]