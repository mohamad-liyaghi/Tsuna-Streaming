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
from accounts.serializers import (
    RegisterUserSerializer,
    VerifyUserSerializer,
    ResendTokenSerializer,
)
from accounts.throttling import AuthenticationThrottle
from accounts.models import VerificationToken


USER = get_user_model()


@extend_schema_view(
    post=extend_schema(
        description="""Register an account to the system.""",
        responses={
            201: "Created",
            400: "Bad Request",
            403: "Forbidden",
        },
        tags=["Authentication"],
    ),
)
class RegisterUserView(CreateAPIView):
    """
    Users can register to the system.
    """

    permission_classes = [AllowUnAuthenticatedPermission]
    serializer_class = RegisterUserSerializer
    throttle_classes = [AuthenticationThrottle]


@extend_schema_view(
    get=extend_schema(
        description="""Verify an account""",
        responses={
            200: "OK",
            400: "Bad Request",
            403: "Forbidden",
            404: "Token or user not found",
        },
        tags=["Authentication"],
    ),
)
class VerifyUserView(APIView):
    """Verify an account"""

    permission_classes = [AllowUnAuthenticatedPermission]
    throttle_classes = [AuthenticationThrottle]

    serializer_class = VerifyUserSerializer

    def get_object(self):
        """Get the token object"""
        return get_object_or_404(
            VerificationToken, token=self.kwargs["verification_token"]
        )

    def get(self, request, *args, **kwargs):
        """Get the url"""
        verification_token = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.verify_code(
                user_token=kwargs["user_token"],
                token=verification_token,
            )
            return Response("Account verified", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        description="""
        Resend verification token to user if the other one is expired.
        """,
        responses={
            201: "OK",
            400: "Bad Request",
            403: "Forbidden",
        },
        tags=["Authentication"],
    ),
)
class ResendTokenView(CreateAPIView):
    """
    Resend verification token to user if the other one is expired.
    """

    permission_classes = [AllowUnAuthenticatedPermission]
    throttle_classes = [AuthenticationThrottle]

    serializer_class = ResendTokenSerializer


@extend_schema_view(
    post=extend_schema(
        description="""Return JWT token to users for loging in.""",
        tags=["Authentication"],
    ),
)
class LoginUserView(TokenObtainPairView):
    """
    Get JWT token for users.
    """

    permission_classes = [AllowUnAuthenticatedPermission]
    throttle_classes = [AuthenticationThrottle]
