from django.contrib import admin
from votes.models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "choice", "content_type"]
