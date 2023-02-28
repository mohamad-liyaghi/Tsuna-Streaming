from django.db import models
from django.contrib.contenttypes.models import ContentType
from cached_property import cached_property_with_ttl
from core.exceptions import AdminNotFound, ObjectPermissionDenied


class BaseContentModel(models.Model):
    '''
        The base content model of content models (video, broadcast etc...).
        The only diffrence between this model and models.Model is the methods.
        get_model_content_type_id -> return models Content type id for vote and comment stuff.
        get_viewer_count -> return views of an object (eg: video).
    '''

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if self.pk:
            # update is_updated field if an object is updated
            self.is_updated = True
            return super(BaseContentModel, self).save(*args, **kwargs)
        
        if not self.pk: 
            # get the object channels admin
            admin = self.user.admin.filter(channel=self.channel).first()

            if admin:
                # check if user has permission
                if admin.permissions.filter(model=self.get_model_content_type, add_object=True).exists():
                    return super(BaseContentModel, self).save(*args, **kwargs)        
                
                raise ObjectPermissionDenied("Admin dont have permission to add video.")

            raise AdminNotFound("Admin didnt found.")

        return super(BaseContentModel, self).save(*args, **kwargs)

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
