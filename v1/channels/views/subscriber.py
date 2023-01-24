from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from channels.models import Channel
from channels.models import ChannelSubscriber


class SubscriberView(APIView):
    permission_classes = [IsAuthenticated,]

    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel, token=self.kwargs["channel_token"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        '''Check weather or not user subscribed a channel.'''

        subscriber = ChannelSubscriber.objects.filter(channel=self.channel,
                                         user=self.request.user).exists()
        if subscriber:
            return Response(True, status=status.HTTP_200_OK)

        return Response(False, status=status.HTTP_200_OK)