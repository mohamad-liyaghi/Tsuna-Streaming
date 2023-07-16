from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from drf_spectacular.utils import extend_schema, extend_schema_view


from accounts.permissions import AllowUnAuthenticatedPermission
from accounts.serializers import RegisterUserSerializer
from accounts.throttling import AuthenticationThrottle
from accounts.models import VerificationToken


USER = get_user_model()


@extend_schema_view(
    post=extend_schema(
        description='''Register an account to the system.''',
        responses={
            201: 'Created',
            400: 'Bad Request',
            403: 'Forbidden',
        }
    ),
)
class RegisterUserView(CreateAPIView):
    """
        Users can register to the system.
    """

    permission_classes = [AllowUnAuthenticatedPermission]
    serializer_class = RegisterUserSerializer
    throttle_classes = [AuthenticationThrottle]


# TODO: Update this and add resend
@extend_schema_view(
    get=extend_schema(
        description='''Get the token from url and check whether  or not the token is active and do the activation process.'''
    ),
)
class VerifyUserView(APIView):
    '''Verify accounts.'''

    permission_classes = [AllowUnAuthenticatedPermission,]
    throttle_classes = [AuthenticationThrottle,]

    def get(self, request, *args, **kwargs):
        user_id = self.get("user_token")
        token = self.get("token")

        if all([user_id, token]):
            user = get_object_or_404(USER, token=user_id)

            if not user.is_active:
                user_token = VerificationToken.objects.filter(user=user).first()

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
    """
    Get JWT token for users.
    """
    permission_classes = [AllowUnAuthenticatedPermission]
    throttle_classes = [AuthenticationThrottle]
