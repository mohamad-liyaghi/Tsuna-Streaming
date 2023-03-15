from rest_framework import serializers
from channel_admins.models import Admin, Permission
from django.core.exceptions import PermissionDenied
from channel_admins.exceptions import DuplicatePromotionException, SubscriptionRequiredException


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
        kwargs['promoted_by'] = self.context['request_user']
        kwargs['channel'] = self.context['channel']

        # only admins with add_new_admin permission can add admins.
        if not kwargs['promoted_by'].admin.filter(channel=kwargs['channel'], add_new_admin=True).exists():
            raise serializers.ValidationError("You dont have permission to promote admin.")

        try:
            return super().save(**kwargs)

        except DuplicatePromotionException:
            raise serializers.ValidationError("Admin already exists.")

        except SubscriptionRequiredException:
            raise serializers.ValidationError("User hasnt subscribed to the channel yet.")
        
        except PermissionDenied as error:
            raise serializers.ValidationError(str(error))


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
    permissions = PermissionListSerializer(many=True, read_only=True)

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


class AdminPermissionDetailSerializer(serializers.ModelSerializer):
    '''Detail/Update page of an admins permissions.'''
    
    admin = serializers.StringRelatedField()

    class Meta:
        model = Permission
        fields = ['admin', 'add_object', 'edit_object', 'delete_object', 'publish_object']