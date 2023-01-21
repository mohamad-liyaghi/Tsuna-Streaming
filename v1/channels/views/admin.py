from rest_framework.generics import ListCreateAPIView
from channels.serializers.admin import ChannelAdminListSerializer, ChannelAdminCreateSerializer
from channels.models import Channel, ChannelAdmin
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404


class ChannelAdminView(ListCreateAPIView):
    '''Get channel admins and add an admin'''

    def dispatch(self, request, *args, **kwargs):
        # get the given cahnnel
        self.channel = get_object_or_404(Channel, token=self.kwargs["token"])

        # check if user has permission to access a channel admin list
        if request.user == self.channel.owner or \
                     request.user in [i.user for i in self.get_queryset()]:
            return super().dispatch(request, *args, **kwargs)

        return JsonResponse({"Forbidden" : "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        # check if admin can add admin or not
        current_admin = self.request.user.channel_admin.filter(
            channel=self.channel, add_new_admin=True
            ).first()

        if request.user == self.channel.owner or current_admin:
            serializer = ChannelAdminCreateSerializer(data=request.data)
            
            if serializer.is_valid():
                # TODO check user is subscriber of not
                serializer.save(promoted_by=self.request.user, channel=self.channel)
                return JsonResponse({"Forbidden" : "Admin added."}, status=status.HTTP_201_CREATED)        

            return JsonResponse({"Forbidden" : "Data is not valid."}, status=status.HTTP_201_CREATED)        
        
        return JsonResponse({"Forbidden" : "You dont have permission to add admin."},
                                status=status.HTTP_403_FORBIDDEN)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChannelAdminListSerializer

        elif self.request.method == "POST":
            return ChannelAdminCreateSerializer


    def get_queryset(self):    
        return ChannelAdmin.objects.filter(channel=self.channel)
