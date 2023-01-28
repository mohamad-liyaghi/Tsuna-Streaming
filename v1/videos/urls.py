from django.urls import path
from rest_framework.routers import SimpleRouter
from videos.views import VideoViewSet

app_name = "v1_videos"
router = SimpleRouter()

router.register("video",VideoViewSet, basename="video")

urlpatterns = [
    
]

urlpatterns += router.urls