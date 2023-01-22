from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.serializers.admin import ChannelAdminListSerializer, ChannelAdminCreateSerializer, ChannelAdminDetailView
from channels.models import Channel, ChannelAdmin
from channels.permissions import ChennelAdminPermission, ChannelAdminDetailPermission


class ChannelAdminView(ListCreateAPIView):
    '''Get channel admins and add an admin'''
    permission_classes = [IsAuthenticated, ChennelAdminPermission,] 

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChannelAdminListSerializer

        elif self.request.method == "POST":
            return ChannelAdminCreateSerializer

    def get_queryset(self):    
        channel = get_object_or_404(Channel, token=self.kwargs["token"])
        return ChannelAdmin.objects.select_related(
                                        "channel", "channel__owner"
                                    ).filter(channel=channel)


    def post(self, request, *args, **kwargs):
        '''Create a new admin [Admins who have permission]'''
        # check if admin can add admin or not
        channel = self.get_queryset().first().channel

        current_admin = self.request.user.channel_admin.filter(
            channel=channel, add_new_admin=True
            ).first()

        if request.user == channel.owner or current_admin:
            serializer = ChannelAdminCreateSerializer(data=request.data)  

            if serializer.is_valid():
                # TODO check user is subscriber of not
                # check if admin does not exists
                if ChannelAdmin.objects.filter(user=serializer.validated_data["user"],
                            promoted_by=self.request.user, channel=channel):

                            return JsonResponse({"Forbidden" : "Admin already exists."}, 
                                    status=status.HTTP_403_FORBIDDEN)       

                serializer.save(promoted_by=self.request.user, channel=channel)
                return JsonResponse({"success" : "Admin added."}, status=status.HTTP_201_CREATED)        

            return JsonResponse({"Forbidden" : "Data is not valid."}, status=status.HTTP_403_FORBIDDEN)        
        
        return JsonResponse({"Forbidden" : "You dont have permission to add admin."},
                                status=status.HTTP_403_FORBIDDEN)
        
    def get(self, request, *args, **kwargs):
        '''List of admins of a channel [Admins]'''
        return super().get(request, *args, **kwargs)



@extend_schema_view(
    get=extend_schema(
        description="Admin permission list, [Admin and channel owner]."
    ),
    put=extend_schema(
        description="Update an admins permission, [Channel owner]."
    ),
    patch=extend_schema(
        description="Update an admins permission, [Channel owner]."
    ),
    destroy=extend_schema(
        description="Delete an admin, [Channel owner]."
    ),
)
class ChannelAdminDetailView(RetrieveUpdateDestroyAPIView):
    '''Detail page of admins'''

    serializer_class = ChannelAdminDetailView
    permission_classes = [IsAuthenticated, ChannelAdminDetailPermission]
    
    def get_queryset(self):
        return Channel.objects.filter(token=self.kwargs["channel_token"])


    def get_object(self):
        channel = get_object_or_404(Channel, token=self.kwargs["channel_token"])
        admin = get_object_or_404(ChannelAdmin, channel=channel, token=self.kwargs["admin_token"])

        if self.request.user == channel.owner or \
                 self.request.user == admin.user:
            return admin

        raise Http404("No result found.")


    def destroy(self, request, *args, **kwargs):
        '''Delete an admin [Owner only]'''
        return super().destroy(request, *args, **kwargs)    


    def put(self, request, *args, **kwargs):
        '''Update an admin [Admin]'''
        return super().put(request, *args, **kwargs)
        

    def patch(self, request, *args, **kwargs):
        '''Update an admin [Admin]'''
        return super().put(request, *args, **kwargs)