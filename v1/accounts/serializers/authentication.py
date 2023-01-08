from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import Token


USER = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    '''User registration serializer'''
    
    email = serializers.EmailField()

    class Meta:
        model = USER
        fields = ["email", "first_name", "last_name", "picture", "bio"]


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
                token = Token.objects.filter(user=user).first()

                if token and token.is_valid:
                    raise serializers.ValidationError("We have already sent you a token to {}, please verify your account".format(email))

                else:
                    Token.objects.create(user=user)
                    raise serializers.ValidationError("We have sent you a token to {}, please verify your account.".format(email))

        return value
