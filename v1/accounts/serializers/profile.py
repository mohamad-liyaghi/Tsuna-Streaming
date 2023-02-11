from django.contrib.auth import get_user_model
from rest_framework import serializers
from .subscription import UserSubscriptionListSerializer

USER = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField(method_name="active_subscription")

    class Meta:
        model = USER
        fields = ["email", "first_name", "last_name", 
                "picture", "bio", "get_role_display", "token", 
                "subscription"]
                
        extra_kwargs = {
            'email': {'read_only': True},
            'token': {'read_only': True},            
            'subscription' : {'read_only': True},
        }
    
    def active_subscription(self, user:USER):
        '''Show the active subscription (title, date)'''
        if user.role == "p":
            subscription = user.subscriptions.select_related("plan").first()

            if subscription.is_active:
                serialized_data = UserSubscriptionListSerializer(subscription)
                return serialized_data.data

            return None

        return None