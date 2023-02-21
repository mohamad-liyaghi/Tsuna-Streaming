from django.apps import AppConfig


class AdminsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admins'

    def ready(self) -> None:
        import admins.signals