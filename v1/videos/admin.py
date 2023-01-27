from django.contrib import admin
from videos.models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "channel", "user", "is_published"]
