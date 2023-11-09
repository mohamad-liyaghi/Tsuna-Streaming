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
        fields = ["user", "promoted_by", "channel", "token"]


class AdminCreateSerializer(serializers.ModelSerializer):
    """
    Create a new admin.
    """

    user = serializers.SlugRelatedField(
        slug_field="token", queryset=Account.objects.all()
    )

    class Meta:
        model = ChannelAdmin
        fields = ["user"]

    def save(self, **kwargs):
        kwargs.setdefault("promoted_by", self.context["request_user"])
        kwargs.setdefault("channel", self.context["channel"])

        try:
            return super().save(**kwargs)
        except Exception as e:
            raise serializers.ValidationError(str(e))


class PermissionListSerializer(serializers.ModelSerializer):
    """
    List of all permissions of an admin
    """

    class Meta:
        model = ChannelAdminPermission
        fields = [
            "can_add_object",
            "can_edit_object",
            "can_delete_object",
            "can_publish_object",
            "can_change_channel_info",
        ]


class AdminDetailSerializer(serializers.ModelSerializer):
    """
    Retrieve an admin alongside its permissions
    """

    permissions = PermissionListSerializer()

    user = serializers.StringRelatedField()
    promoted_by = serializers.StringRelatedField()

    class Meta:
        model = ChannelAdmin
        fields = [
            "user",
            "promoted_by",
            "date",
            "permissions",
        ]
        read_only_fields = [
            "user",
            "promoted_by",
            "date",
        ]

    def update(self, instance, validated_data):
        """
        Update the permissions of an admin.
        """
        permissions_data = validated_data.pop("permissions")
        permissions = instance.permissions

        # Update permissions
        for permission in permissions_data:
            setattr(permissions, permission, permissions_data[permission])
        permissions.save()
        return instance
