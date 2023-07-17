from django.contrib.auth import get_user_model
from rest_framework import serializers


USER = get_user_model()


# TODO: UnComment this
# class UserSubscriptionListSerializer(serializers.Serializer):
#     plan = serializers.CharField(read_only=True)
#     start_date = serializers.DateTimeField(read_only=True)
#     finish_date = serializers.DateTimeField(read_only=True)
#


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User Profile (Get, Update)
    """

    class Meta:
        model = USER
        fields = [
            "email",
            "first_name",
            "last_name",
            "picture",
            "bio",
            "token",
            #"active_subscription" #TODO: update this
        ]
        read_only_fields = [
            "email",
            "token",
        ]
