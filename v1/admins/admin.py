from django.contrib import admin
from admins.models import Admin

@admin.register(Admin)
class ChannelAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel', 'date']