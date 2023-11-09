from django.contrib.auth import get_user_model
from rest_framework import serializers
from memberships.models import Subscription


USER = get_user_model()


class UserSubscriptionListSerializer(serializers.Serializer):
    membership = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User Profile (Get, Update)
    """

    active_subscription = serializers.SerializerMethodField(
        method_name="get_active_subscription", read_only=True
    )

    class Meta:
        model = USER
        fields = [
            "email",
            "first_name",
            "last_name",
            "picture",
            "bio",
            "token",
            "active_subscription",
        ]
        read_only_fields = [
            "email",
            "token",
        ]

    def get_active_subscription(self, obj):
        """
        Returns the active subscription for the given user.
        """
        serializer = UserSubscriptionListSerializer(
            Subscription.objects.get_active_subscription(user=obj)
        )
        return serializer.data
