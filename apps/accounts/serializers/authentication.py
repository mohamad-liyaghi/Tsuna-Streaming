from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for registering users."""
    
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = USER
        fields = (
            "email",
            "first_name",
            "last_name",
            "picture",
            "bio",
            "password"
        )

    def validate_email(self, value):
        """
        Make sure that email is unique and not used before.
        """

        email = value
        user = USER.objects.filter(email=email).first()

        if user:
            if user.is_active:
                raise serializers.ValidationError(
                    f"An active account with email `{email}` already exists."
                )

            raise serializers.ValidationError(
                f"A deactive account with email `{email}` already exists."
            )

        return value

    def create(self, validated_data):
        return USER.objects.create_user(**validated_data)
