from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import VerificationToken


USER = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    '''User registration serializer'''
    
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = USER
        fields = ["email", "first_name", "last_name", "picture", "bio", "password"]


    def validate_email(self, value):
        '''
            Check if user with the same email exists or not.
            If exists, is it active or not.
            Active users must Login
            Deactive users must verify themselves
        '''

        email = value
        user = USER.objects.filter(email=email).first()

        if user:
            if user.is_active:
                raise serializers.ValidationError("An active account with email {} founded".format(email))

            elif not user.is_active:
                token = VerificationToken.objects.filter(user=user).first()

                if token and token.is_valid:
                    raise serializers.ValidationError("We have already sent you a token to {}, please verify your account".format(email))

                else:
                    VerificationToken.objects.create(user=user)
                    raise serializers.ValidationError("We have sent you a token to {}, please verify your account.".format(email))

        return value

    def create(self, validated_data):
        user = super(RegisterUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user