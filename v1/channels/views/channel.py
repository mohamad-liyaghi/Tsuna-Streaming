from rest_framework.viewsets import ModelViewSet
from channels.models import Channel
from accounts.permissions import AllowAuthenticatedPermission


class ChannelViewSet(ModelViewSet):
    '''A viewset for Creating, Updating, retrieving a channel'''

    permission_classes = [AllowAuthenticatedPermission,]
    queryset = Channel.objects.all()