from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from viewers.models import Viewer

def check_viewer_status(view):
    '''This decorator checks if user hasnt viewed an object, a new viewer object will be created'''
    
    def check_view_exists_or_not(self, request, *args, **kwargs):        
        object = self.get_object()
        content_type_model = get_object_or_404(ContentType, model=str(object.__class__.__name__).lower())

        # check is there a view for the object
        viewer = Viewer.objects.filter(content_type=content_type_model, object_id=object.id)

        if viewer:
            return view(self, request, *args, **kwargs)

        # create a user view for an object if does not exist            
        Viewer.objects.create(user=request.user, content_type=content_type_model, object_id=object.id)
        return view(self, request, *args, **kwargs)

    return check_view_exists_or_not