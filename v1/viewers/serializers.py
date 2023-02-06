from rest_framework import serializers
from viewers.models import Viewer


class ViewerListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Viewer
        fields = ['user', 'date']