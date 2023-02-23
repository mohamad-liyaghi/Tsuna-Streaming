from rest_framework import serializers
from admins.models import Admin
from admins.exceptions import AdminAlreadyExists, AdminNotSubscribed


class AdminListSerializer(serializers.ModelSerializer):
    '''List of a channels admins'''
    user = serializers.StringRelatedField()
    promoted_by = serializers.StringRelatedField()
    
    class Meta:
        model = Admin
        fields = ['user', 'promoted_by', 'channel', 'token']

class AdminCreateSerializer(serializers.ModelSerializer):
    '''Create an admin serializer'''

    class Meta:
        model = Admin
        fields = ['user', 'change_channel_info', 'add_new_admin', 'block_user']

    def save(self, **kwargs):
        return super().save(**kwargs)

    def save(self, **kwargs):
        kwargs['promoted_by'] = self.context['request_user']
        kwargs['channel'] = self.context['channel']

        try:
            return super().save(**kwargs)

        except AdminAlreadyExists:
            raise serializers.ValidationError("Admin already exists.")

        except AdminNotSubscribed:
            raise serializers.ValidationError("User hasnt subscribed to the channel yet.")
        
        except:
            raise serializers.ValidationError("Permission denied.")