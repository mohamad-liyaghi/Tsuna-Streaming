from django.db import models
from django.contrib.contenttypes.models import ContentType
from admins.models import Admin


class Permission(models.Model):
    '''
        Admin permission model.
        After creating admin object, an instance of this model will be created for content models via signals.
        E.g: Permission set wether or not an object can be deleted.
    '''

    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='permissions')
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='permissions')

    token = models.CharField(max_length=32, blank=True, null=True)

    add_object = models.BooleanField(default=False)
    edit_object = models.BooleanField(default=False)
    delete_object = models.BooleanField(default=False)
    publish_object = models.BooleanField(default=False)

    delete_object_comment = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["admin", "model"],
                name="unique_admin_model"
            )
        ]

    def __str__(self) -> str:
        return str(self.admin.user)

    def get_model_name(self):
        '''A method that returns models name for viewing in serializer'''
        return self.model.model
    