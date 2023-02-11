from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from drf_spectacular.utils import extend_schema, extend_schema_view


from accounts.permissions import AllowUnAuthenticatedPermission
from accounts.serializers import RegisterUserSerializer
from accounts.models import Token


USER = get_user_model()

@extend_schema_view(
    get=extend_schema(
        description='''Simply ask for credentials.'''
    ),
    post=extend_schema(
        description='''Check and verify users credentials.'''
    ),
)
class RegisterUserView(APIView):
    '''Register new accounts'''

    permission_classes = [AllowUnAuthenticatedPermission,]
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



@extend_schema_view(
    get=extend_schema(
        description='''Get the token from url and check whether  or not the token is active and do the activation process.'''
    ),
)
class VerifyUserView(APIView):
    '''Verify accounts.'''

    permission_classes = [AllowUnAuthenticatedPermission,]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_token")
        token = self.kwargs.get("token")

        if all([user_id, token]):
            user = get_object_or_404(USER, token=user_id)

            if not user.is_active:
                user_token = Token.objects.filter(user=user).first()

                if user_token:

                    if user_token.is_valid:

                        if user_token.token == token:
                            user.is_active = True
                            user.save()
                            return Response("Account verified successfully.", status=status.HTTP_200_OK)

                        user_token.retry += 1
                        user_token.save()
                        return Response("Invalid token were given.", status=status.HTTP_403_FORBIDDEN)  

                    return Response("Token was expired.", status=status.HTTP_403_FORBIDDEN)
                                  
                return Response("We couldnt find a valid token for given user.", status=status.HTTP_403_FORBIDDEN)
                
            return Response("Invalid user was given.", status=status.HTTP_403_FORBIDDEN)

        return Response("Invalid Information", status=status.HTTP_403_FORBIDDEN)


@extend_schema_view(
    post=extend_schema(
        description='''Return JWT token to users for loging in.'''
    ),
)
class LoginUserView(TokenObtainPairView):
    '''Users can request to this endpoint in order to get new access key'''
    permission_classes = [AllowUnAuthenticatedPermission,]
    pass