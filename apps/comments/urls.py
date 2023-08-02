from django.urls import path
from .views import CommentListCreateView, CommentDetailView, CommentPinView

app_name = "comments"

urlpatterns = [
    path(
        "<str:content_type_id>/<str:object_token>/",
        CommentListCreateView.as_view(),
        name="comment_list_create"
    ),

    path(
         "<str:content_type_id>/<str:object_token>/<str:comment_token>/",
         CommentDetailView.as_view(),
         name="comment_detail"
    ),
                 
    path('<str:object_token>/<str:comment_token>/pin/',
                 CommentPinView.as_view(), name="comment_pin"),
    
]
