from django.contrib import admin
from accounts.models import Account, VerificationToken


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "token"]

    def has_change_permission(self, request, obj=None):
        """No body can change info in admin panel"""
        return False


@admin.register(VerificationToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ["user", "expire_at", "is_valid"]

    def has_change_permission(self, request, obj=None):
        """No body can change info in admin panel"""
        return False
    