from django.core.exceptions import ValidationError
from django.conf import settings
from videos.constants import VIDEO_LIMIT_NORMAL_USER, VIDEO_LIMIT_PREMIUM_USER


def validate_video_size(file, user: settings.AUTH_USER_MODEL) -> None:
    """
    Validate file size
    """
    file_size = file.size / (1024 * 1024)

    if user.is_premium() and file_size > int(VIDEO_LIMIT_PREMIUM_USER):
        raise ValidationError(
            f"Video file size should not exceed {VIDEO_LIMIT_PREMIUM_USER}MB."
        )

    if user.is_normal() and file_size > int(VIDEO_LIMIT_NORMAL_USER):
        raise ValidationError(
            f"Normal users can upload videos up to {VIDEO_LIMIT_NORMAL_USER}MB."
        )
