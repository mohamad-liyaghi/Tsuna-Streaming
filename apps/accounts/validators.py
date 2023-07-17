from django.core.exceptions import ValidationError

def validate_profile_size(file):
    """Validate profile picture size."""
    limit = 5242880

    if file.size > limit:
        raise ValidationError(f"Profile picture can not be larger than 5 MB.")