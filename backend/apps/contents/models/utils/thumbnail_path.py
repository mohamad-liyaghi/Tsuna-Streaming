
def get_thumbnail_upload_path(instance, filename):
    """
    Return the uploaded thumbnail path
    eg: thumbnails/music/1.jpg
    """
    return f"thumbnails/{instance.__class__.__name__.lower()}/{filename}"
