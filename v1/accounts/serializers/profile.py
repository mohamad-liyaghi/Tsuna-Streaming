from django.contrib.auth import get_user_model
from rest_framework import serializers


USER = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ["email", "first_name", "last_name", 
                "picture", "bio", "get_role_display", "user_id"]