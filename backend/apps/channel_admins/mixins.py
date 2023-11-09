from django.shortcuts import get_object_or_404
from channels.models import Channel


class ChannelMixin:
    """
    Get the channel passed in the url.
    """

    def dispatch(self, request, *args, **kwargs):
        # Set channel to self.channel
        self.channel = get_object_or_404(Channel, token=kwargs["channel_token"])
        return super(ChannelMixin, self).dispatch(request, *args, **kwargs)
