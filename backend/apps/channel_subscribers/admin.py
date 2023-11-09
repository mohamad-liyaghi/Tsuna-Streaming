from django.contrib import admin
from channel_subscribers.models import ChannelSubscriber


@admin.register(ChannelSubscriber)
class ChannelSubscriberAdmin(admin.ModelAdmin):
    list_display = ["user", "channel", "date"]
