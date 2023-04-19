from django.contrib import admin
from accounts.models import Account, Token


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["email", "role", "is_active", "token"]

    def has_change_permission(self, request, obj=None):
        '''No body can change info in admin panel'''
        return False


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ["user", "date_created", "is_valid"]

    fieldsets = (
		(None, {'fields':('user', 'token', "retry")}),
	)

    def has_change_permission(self, request, obj=None):
        '''No body can change info in admin panel'''
        return False
    