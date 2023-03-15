from django.contrib import admin
from channel_admins.models import Admin, Permission

@admin.register(Admin)
class ChannelAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel', 'date']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['admin', 'model', 'token']