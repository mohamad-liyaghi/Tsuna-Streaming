from django.urls import path, include
from .views import CommentListCreateView, CommentDetailView, CommentPinView

app_name = "comments"

V1 = [
    path(
        "<str:content_type_id>/<str:object_token>/",
        CommentListCreateView.as_view(),
        name="comment_list_create",
    ),
    path(
        "<str:content_type_id>/<str:object_token>/<str:comment_token>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "<str:content_type_id>/<str:object_token>/<str:comment_token>/pin/",
        CommentPinView.as_view(),
        name="comment_pin",
    ),
]

urlpatterns = [
    path("v1/", include(V1)),
]
