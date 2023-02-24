from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework import status
from channels.models import Channel

class AdminPermissionMixin:
    '''
        Only Admin users can see the list of admins.
        This mixin gets the channel object and check if user is admin or not.
    '''

    def dispatch(self, request, *args, **kwargs):
        # the given channel by user
        self.channel = get_object_or_404(Channel, token=self.kwargs['channel_token'])
        
        # check if user is admin of the given channel
        if request.user.admin.filter(channel=self.channel).exists():
            return super(AdminPermissionMixin, self).dispatch(request, *args, **kwargs)
        
        return JsonResponse({'permission denied' : 'You can not access this page.'}, status=status.HTTP_403_FORBIDDEN)
    


class UpdateAdminMixin:
    '''Only promoted_user or channel admin can update an admins permissions.'''

    def dispatch(self, request, *args, **kwargs):
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            
            object = self.get_object()
        
            if request.user not in [object.promoted_by, object.channel.owner]:

                return HttpResponseForbidden("Permission denied.", status=status.HTTP_403_FORBIDDEN)

        return super().dispatch(request, *args, **kwargs)