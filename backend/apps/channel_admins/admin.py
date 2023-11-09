from django.contrib import admin
from channel_admins.models import ChannelAdmin, ChannelAdminPermission


@admin.register(ChannelAdmin)
class ChannelAdminAdmin(admin.ModelAdmin):
    list_display = ["user", "channel", "date"]


@admin.register(ChannelAdminPermission)
class ChannelAdminPermissionAdmin(admin.ModelAdmin):
    list_display = ["admin", "token"]
