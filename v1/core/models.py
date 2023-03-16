from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from cached_property import cached_property_with_ttl




class BaseContentModel(models.Model):
    '''
        The base content model of content models (video, broadcast etc...).
        This model contains some common fields.
        The only diffrence between this model and models.Model is the methods.
    '''

    class Visibility(models.TextChoices):
        PRIVATE = ("pr", "Private")
        PUBLISHED = ("pu", "Public")

    visibility = models.CharField(max_length=2, choices=Visibility.choices, default=Visibility.PRIVATE)
    is_updated = models.BooleanField(default=False)

    # whether or not user can add comment
    allow_comment = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True)


    @cached_property_with_ttl(ttl=60 * 60 * 24)
    def get_model_content_type_id(self):
        '''Return content type id of the model (Eg: Video)'''

        cls = self.__class__
        return ContentType.objects.get_for_model(cls).id if cls else None


    @cached_property_with_ttl(ttl=60 * 60 * 24)
    def get_model_content_type(self):
        '''Return content type instance of a model (Eg: Video)'''

        cls = self.__class__
        return ContentType.objects.get_for_model(cls) if cls else None


    @cached_property_with_ttl(ttl=60)
    def get_viewer_count(self):    
        '''Return objects viewers cout'''

        return self.viewer.count()


    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if self.pk:
            # update is_updated field if an object is updated
            self.is_updated = True
            return super(BaseContentModel, self).save(*args, **kwargs)
        
        if not self.pk: 
            # get the object channels admin
            admin = self.user.channel_admins.filter(channel=self.channel).first()

            if admin:
                # check if user has permission
                if admin.permissions.filter(model=self.get_model_content_type, add_object=True).exists():
                    return super(BaseContentModel, self).save(*args, **kwargs)        
                
                raise PermissionDenied("Admin dont have permission to add video.")

            raise PermissionDenied("Admin didnt found.")

        return super(BaseContentModel, self).save(*args, **kwargs)


