from rest_framework import serializers
from channels.models import ChannelAdmin

class ChannelAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = ["user", "date", "token"]