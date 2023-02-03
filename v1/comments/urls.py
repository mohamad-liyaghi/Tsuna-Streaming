from django.urls import path
from .views import CommentView, CommentDetailView

app_name = "v1_comments"

urlpatterns = [
    path('comment/<str:content_type_id>/<str:object_token>/', CommentView.as_view(), name="comment"),
    path('comment/<str:content_type_id>/<str:object_token>/<str:comment_token>',
                 CommentDetailView.as_view(), name="comment_detail"),
]
