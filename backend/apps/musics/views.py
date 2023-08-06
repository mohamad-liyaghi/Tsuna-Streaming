from drf_spectacular.utils import extend_schema, extend_schema_view
from contents.views import (
    ContentListCreateView,
    ContentDetailView
)
from musics.models import Music
from musics.serializers import (
    MusicListSerializer,
    MusicCreateSerializer,
    MusicDetailSerializer
)


@extend_schema_view(
    get=extend_schema(
        description="List of a channel's musics.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
    post=extend_schema(
        description="Create a new music.",
        responses={
            201: 'Created',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
)
class MusicListCreateView(ContentListCreateView):
    """
    List/Create a music
    """
    model = Music

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MusicListSerializer

        return MusicCreateSerializer


@extend_schema_view(
    get=extend_schema(
        description="Retrieve a musics.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
    put=extend_schema(
        description="Update a music by channel admin.",
        responses={
            200: 'ok',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
    patch=extend_schema(
        description="Update a music by channel admin.",
        responses={
            200: 'ok',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
    delete=extend_schema(
        description="Delete a music by channel admins.",
        responses={
            204: 'No content',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
)
class MusicDetailView(ContentDetailView):
    model = Music
    serializer_class = MusicDetailSerializer
