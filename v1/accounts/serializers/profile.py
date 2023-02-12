from django.contrib.auth import get_user_model
from rest_framework import serializers
from .subscription import UserSubscriptionListSerializer

USER = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    active_subscription = UserSubscriptionListSerializer()

    class Meta:
        model = USER
        fields = ["email", "first_name", "last_name", 
                "picture", "bio", "get_role_display", "token", 
                "active_subscription"]
                
        extra_kwargs = {
            'email': {'read_only': True},
            'token': {'read_only': True},            
            'subscription' : {'read_only': True},
        }
    