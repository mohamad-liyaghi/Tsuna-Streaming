from rest_framework import serializers
from admins.models import Admin


class AdminListSerializer(serializers.ModelSerializer):
    '''List of a channels admins'''
    user = serializers.StringRelatedField()
    promoted_by = serializers.StringRelatedField()
    
    class Meta:
        model = Admin
        fields = ['user', 'promoted_by', 'channel', 'token']