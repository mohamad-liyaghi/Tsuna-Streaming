def get_file_upload_path(instance, filename):
    """
    Return the uploaded files path
    eg: files/music/1.mp3
    """
    return f"files/{instance.__class__.__name__.lower()}/{filename}"
