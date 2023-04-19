from django.shortcuts import get_object_or_404
from channels.models import Channel

class ChannelObjectMixin:
    '''Get the channel that user wants its videos'''
    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel, token=self.kwargs['channel_token'])
        return super().dispatch(request, *args, **kwargs)