from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.core.tasks import send_email
from musics.models import Music


@receiver(post_save, sender=Music)
def notify_music_creation(sender, instance, created, **kwargs):
    if created:
        data = {
            "first_name": instance.user.first_name,
            "channel_title": instance.title,
            "channel_token": instance.channel.token,
            "music_token": instance.token,
        }

        if instance.user == instance.channel.owner:
            send_email.delay(
                template_name="emails/notify_music_creation.html",
                to_email=instance.user.email,
                body=data,
            )

        else:
            # send email to both admin and owner
            send_email.delay(
                template_name="emails/notify_music_creation.html",
                to_email=instance.user.email,
                body=data,
            )

            send_email.delay(
                template_name="emails/notify_music_creation.html",
                to_email=instance.channel.owner.email,
                body=data,
            )
