from rest_framework.generics import ListCreateAPIView
from channels.serializers.admin import ChannelAdminListSerializer
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
    

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChannelAdminListSerializer


    def get_queryset(self):    
        return ChannelAdmin.objects.filter(channel=self.channel)
