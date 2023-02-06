from viewers.models import Viewer

def check_viewer_status(view):
    '''This decorator checks if user hasnt viewed an object, a new viewer object will be created'''
    
    def check_view_exists_or_not(self, request, *args, **kwargs):        
        object = self.get_object()

        # check is there a view for the object
        viewer = object.viewer.filter(user=request.user)

        if viewer:
            return view(self, request, *args, **kwargs)

        # create a user view for an object if does not exist            
        Viewer.objects.create(user=request.user, content_object=object)

        return view(self, request, *args, **kwargs)

    return check_view_exists_or_not