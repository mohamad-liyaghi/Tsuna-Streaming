from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.permissions import NotAuthenticated
from accounts.serializers import RegisterUserSerializer
from accounts.models import Token


USER = get_user_model()


class RegisterUserView(APIView):
    '''Register new accounts'''

    permission_classes = [NotAuthenticated,]
    serializer_class = RegisterUserSerializer


    def get(self, request, *args, **kwargs):
        '''Simply ask for credentials'''
        return Response("Enter your credentials.", status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):
        '''
            Validate email and register a user if data was valid.
            First it checks if there is any user registered with given email:
                1- if it was active, user must log in.
                2- if not active, user should verify
            Otherwise user can register
        '''
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response("We have send you an email, please check your inbox and verify your account",
                             status=status.HTTP_201_CREATED)

        return Response(serialized_data.errors, status=status.HTTP_403_FORBIDDEN)


class VerifyUserView(APIView):
    '''Verify accounts.'''

    permission_classes = [NotAuthenticated,]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        token = self.kwargs.get("token")

        if user_id and token:
            user = USER.objects.filter(user_id=user_id).first()

            if user and not user.is_active:
                token = Token.objects.filter(token=token, user=user).first()

                if token.is_valid:
                    user.is_active = True
                    user.save()
                    return Response("Account verified successfully.", status=status.HTTP_200_OK)
                    
                return Response("Token is expired.", status=status.HTTP_403_FORBIDDEN)

            return Response("Token is expired.", status=status.HTTP_403_FORBIDDEN)

        return Response("Invalid Information", status=status.HTTP_403_FORBIDDEN)


class LoginUserView(TokenObtainPairView):
    '''Users can request to this endpoint in order to get new access key'''
    permission_classes = [NotAuthenticated,]
    pass