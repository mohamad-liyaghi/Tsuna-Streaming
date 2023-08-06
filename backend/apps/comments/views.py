from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    UpdateAPIView
)

from comments.serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    CommentPinSerializer
)
from comments.permissions import (
    CommentCreatePermission,
    IsCommentOwner,
    CanPinComment
)

from apps.core.mixins import ContentObjectMixin


@extend_schema_view(
    get=extend_schema(
        description="List an object's comments.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            404: 'Not found'
        },
        tags=['Comments']
    ),
    post=extend_schema(
        description="Create/Reply a comment.",
        responses={
            201: 'Created',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
            404: 'Not found'
        },
        tags=['Comments']
    )
)
class CommentListCreateView(ContentObjectMixin, ListCreateAPIView):
    """
    Create And List Comments.
    """

    def get_permissions(self):
        # check if comments are allowed for object if request is POST
        if self.request.method == "POST":
            return [IsAuthenticated(), CommentCreatePermission()]
        return [IsAuthenticated()]

    serializer_class = CommentSerializer

    def get_serializer_context(self):
        """
        send user and object to serializer.
        """
        return {'user': self.request.user, 'content_object': self.get_object}

    def get_queryset(self):
        content_object = self.get_object()
        parent_comments = content_object.comments.select_related(
            'user'
        ).filter(parent__isnull=True)
        return parent_comments.order_by("-pinned", "-date")
        

@extend_schema_view(
    get=extend_schema(
        description="Retrieve a comment and its replies.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            404: 'Not found'
        },
        tags=['Comments']
    ),
    put=extend_schema(
        description="Update a comment by its owner.",
        responses={
            200: 'ok',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
            404: 'Not found'
        },
        tags=['Comments']
    ),
    patch=extend_schema(
        description="Update a comment by its owner.",
        responses={
            200: 'ok',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
            404: 'Not found'
        },
        tags=['Comments']
    ),
    delete=extend_schema(
        description="Delete a comment by its owner.",
        responses={
            204: 'No content',
            401: 'Unauthorized',
            403: 'Permission denied',
            404: 'Not found'
        },
        tags=['Comments']
    )
)
class CommentDetailView(ContentObjectMixin, RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        # For PUT, PATCH and DELETE requests
        return [IsAuthenticated(), IsCommentOwner()]

    serializer_class = CommentDetailSerializer

    def get_object(self):
        content_object = super().get_object(bypass_permission=True)

        comment = get_object_or_404(
            content_object.comments.select_related('user').prefetch_related(
            ),
            token=self.kwargs.get("comment_token")
        )
        self.check_object_permissions(self.request, comment)
        return comment


@extend_schema_view(
    put=extend_schema(
        description="Pin a comment by channel staff.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'Permission denied',
            404: 'Not found'
        },
        tags=['Comments']
    ),
    patch=extend_schema(
            description="Pin a comment by channel staff.",
            responses={
                200: 'ok',
                401: 'Unauthorized',
                403: 'Permission denied',
                404: 'Not found'
            },
            tags=['Comments']
    ),
)
class CommentPinView(ContentObjectMixin, UpdateAPIView):
    permission_classes = [IsAuthenticated, CanPinComment]
    serializer_class = CommentPinSerializer

    def get_object(self):
        content_object = super().get_object(bypass_permission=True)

        comment = get_object_or_404(
            content_object.comments.select_related('user').prefetch_related(
            ),
            token=self.kwargs.get("comment_token")
        )
        self.check_object_permissions(self.request, comment)
        return comment
