from django.urls import path
from .views import CommentView

app_name = "v1_comments"

urlpatterns = [
    path('comment/<str:content_type_id>/<str:object_token>/', CommentView.as_view(), name="comment"),
]
