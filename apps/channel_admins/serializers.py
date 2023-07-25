from rest_framework import serializers
from channel_admins.models import ChannelAdmin, ChannelAdminPermission
from accounts.models import Account


class AdminListSerializer(serializers.ModelSerializer):
    """
    List of admins in a channel.
    """
    user = serializers.StringRelatedField()
    promoted_by = serializers.StringRelatedField()

    class Meta:
        model = ChannelAdmin
        fields = ['user', 'promoted_by', 'channel', 'token']


class AdminCreateSerializer(serializers.ModelSerializer):
    """
    Create a new admin.
    """
    user = serializers.SlugRelatedField(
        slug_field='token',
        queryset=Account.objects.all()
    )

    class Meta:
        model = ChannelAdmin
        fields = ['user']

    def save(self, **kwargs):
        kwargs.setdefault('promoted_by', self.context['request_user'])
        kwargs.setdefault('channel', self.context['channel'])

        try:
            return super().save(**kwargs)
        except Exception as e:
            raise serializers.ValidationError(str(e))


class PermissionListSerializer(serializers.ModelSerializer):
    '''Permission list in admin detail page'''

    class Meta:
        model = ChannelAdminPermission
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
        model = ChannelAdmin
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
        model = ChannelAdminPermission
        fields = ['admin', 'add_object', 'edit_object', 'delete_object', 'publish_object']
