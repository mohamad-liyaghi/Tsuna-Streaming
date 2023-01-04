from django.contrib import admin
from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["email", "role", "is_active", "user_id"]

    def has_change_permission(self, request, obj=None):
        '''No body can change info in admin panel'''
        return False