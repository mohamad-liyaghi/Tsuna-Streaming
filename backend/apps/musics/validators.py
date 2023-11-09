from django.core.exceptions import ValidationError
from django.conf import settings
from musics.constants import MUSIC_LIMIT_NORMAL_USER, MUSIC_LIMIT_PREMIUM_USER


def validate_music_size(file, user: settings.AUTH_USER_MODEL) -> None:
    """
    Validate file size
    """
    file_size = file.size / (1024 * 1024)

    if user.is_premium() and file_size > int(MUSIC_LIMIT_PREMIUM_USER):
        raise ValidationError(
            f"Music file size should not exceed {MUSIC_LIMIT_PREMIUM_USER}MB."
        )

    if user.is_normal() and file_size > int(MUSIC_LIMIT_NORMAL_USER):
        raise ValidationError(
            f"Normal users can upload musics up to {MUSIC_LIMIT_NORMAL_USER}MB."
        )
