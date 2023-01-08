from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import NotAuthenticated


class RegisterUserView(APIView):
    permission_classes = [NotAuthenticated,]

    def get(self, request, *args, **kwargs):
        return Response("Enter your credentials.", status=status.HTTP_200_OK)