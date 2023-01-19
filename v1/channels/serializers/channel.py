from rest_framework import serializers
from channels.models import Channel


class ChannelListSerializer(serializers.ModelSerializer):
    # TODO get subs count
    # TODO Add user role in channel
    class Meta:
        model = Channel
        fields = ["profile", "title", "token", "is_verified"]


class ChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["title", "description", "profile", "thumbnail", "token", "date_joined"]
        extra_kwargs = {
            'token': {"read_only" : True},
            'date_joined': {"read_only" : True},
        }


    def create(self, validated_data):
        '''Set request.user as owner of a channel'''

        validated_data["owner"] = self.context["request"].user
        channel = super().create(validated_data)
        return channel


class ChannelDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    
    class Meta:
        model = Channel
        fields = ["title", "description", "profile", "thumbnail", 
                        "owner", "token", "date_joined", "is_verified"]