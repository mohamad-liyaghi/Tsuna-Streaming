from django.db import models
from django.contrib.contenttypes.models import ContentType
from cached_property import cached_property_with_ttl


class BaseContentModel(models.Model):
    '''
        The base content model of content models (video, broadcast etc...).
        The only diffrence between this model and models.Model is the methods.
        get_model_content_type_id -> return models Content type id for vote and comment stuff.
        get_viewer_count -> return views of an object (eg: video).
    '''

    class Meta:
        abstract = True

    @cached_property_with_ttl(ttl=60 * 60 * 24)
    def get_model_content_type_id(self):
        '''Return content type id of a model'''

        cls = self.__class__
        return ContentType.objects.get_for_model(cls).id if cls else None

    @cached_property_with_ttl(ttl=60 * 60 * 24)
    def get_model_content_type(self):
        '''Return content type instance of a model'''

        cls = self.__class__
        return ContentType.objects.get_for_model(cls) if cls else None

    @cached_property_with_ttl(ttl=60)
    def get_viewer_count(self):    
        '''Return objects views '''

        return self.viewer.count()
