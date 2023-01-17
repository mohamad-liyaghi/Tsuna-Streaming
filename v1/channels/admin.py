from django.contrib import admin
from channels.models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    
    list_display = ["title", "owner", "token", "is_verified"]

    def has_change_permission(self, request, obj=None):
        '''No body can change info in admin panel'''
        return False