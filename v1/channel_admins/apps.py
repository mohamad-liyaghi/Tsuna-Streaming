from django.apps import AppConfig


class ChannelAdminsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'channel_admins'

    def ready(self) -> None:
        import channel_admins.signals