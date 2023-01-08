from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import NotAuthenticated
from accounts.serializers import RegisterUserSerializer
from django.contrib.auth import get_user_model

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