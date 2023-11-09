from django.apps import AppConfig


class ChannelSubscribersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "channel_subscribers"

    def ready(self) -> None:
        import channel_subscribers.signals
