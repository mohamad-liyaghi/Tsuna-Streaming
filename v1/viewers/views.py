from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from viewers.serializers import ViewerListSerializer
from core.mixins import ContentObjectMixin


@extend_schema_view(
    get=extend_schema(description="List of an objects viewers."),
)
class ViewerListView(ContentObjectMixin, APIView):
    '''List of an objects viewers'''
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        viewers = []

        # get all viewers in cache with source == cache
        cache_viewers = [
            {
                "user": key.split(":")[2],
                "date": cache_value['date'],
                "source": cache_value['source']
            }
            for key in cache.keys("viewer:*:*")
            if (cache_value := cache.get(key)) and cache_value['source'] == 'cache'
        ]

        # all viewers in db 
        db_viewers = self.object.viewers.select_related('user').all().order_by('-date')

        # append both in viewers list
        viewers += cache_viewers + list(db_viewers)
    
        serializer = ViewerListSerializer(viewers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)