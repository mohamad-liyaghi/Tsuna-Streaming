from django.contrib import admin
from .models import Membership, Subscription


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "active_months", "is_available"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "membership", "end_date", "token"]
