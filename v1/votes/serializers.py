from rest_framework import serializers
from votes.models import Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["choice"]