from viewers.models import Viewer


def ensure_viewer_exists(view):
    """
    Ensures that a viewer exists for the object, and if not, creates one.
    """

    def ensure_viewer_and_continue(self, request, *args, **kwargs):
        # Get the object
        target_object = self.get_object()

        # Attempt to fetch an existing viewer for this object
        viewer = Viewer.objects.get_from_cache(
            channel=target_object.channel,
            object_token=target_object,
            user_token=request.user,
        )

        if not viewer:
            # If no viewer was found, create one
            Viewer.objects.create_in_cache(
                channel=target_object.channel,
                object_token=target_object,
                user_token=request.user,
            )

        return view(self, request, *args, **kwargs)

    return ensure_viewer_and_continue
