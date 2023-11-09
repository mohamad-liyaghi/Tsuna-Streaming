from django.contrib import admin
from viewers.models import Viewer


@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ["user", "content_object", "date"]
