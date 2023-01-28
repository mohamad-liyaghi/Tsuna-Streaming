from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view()
class VideoViewSet(ModelViewSet):
    '''A viewset for adding, updating and retrieving videos'''
    pass