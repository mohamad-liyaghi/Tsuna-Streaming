from django.contrib import admin
from musics.models import Music

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['title', 'channel', 'date', 'token']