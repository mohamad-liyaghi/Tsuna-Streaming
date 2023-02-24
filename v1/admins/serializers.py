from rest_framework import serializers
from admins.models import Admin, Permission
from admins.exceptions import AdminExistsError, AdminNotSubscribedError, PromotePermissionDenied


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

        # only admins with add_new_admin permission can add admins.
        if not kwargs['promoted_by'].admin.filter(channel=kwargs['channel'], add_new_admin=True).exists():
            raise serializers.ValidationError("You dont have permission to promote admin.")

        try:
            return super().save(**kwargs)

        except AdminExistsError:
            raise serializers.ValidationError("Admin already exists.")

        except AdminNotSubscribedError:
            raise serializers.ValidationError("User hasnt subscribed to the channel yet.")
        
        except PromotePermissionDenied:
            raise serializers.ValidationError("You dont have permission to promote admin.")
        

class PermissionListSerializer(serializers.ModelSerializer):
    '''Permission list in admin detail page'''
    class Meta:
        model = Permission
        fields = [
            'get_model_name',
            'token',
        ]

class AdminDetailSerializer(serializers.ModelSerializer):
    '''Admin detail page serializer'''
    # list of user permission tokens
    permissions = PermissionListSerializer(many=True)

    user = serializers.StringRelatedField()
    promoted_by = serializers.StringRelatedField()

    class Meta:
        model = Admin   
        fields = [
            'user',
            'promoted_by',
            'date',
            'change_channel_info',
            'add_new_admin',
            'block_user',
            'permissions',
        ]