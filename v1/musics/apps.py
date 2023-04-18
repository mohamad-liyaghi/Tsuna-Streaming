from django.apps import AppConfig


class MusicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'musics'

    def ready(self) -> None:
        import musics.signals