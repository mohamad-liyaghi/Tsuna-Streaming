from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.core.tasks import send_email
from musics.models import Music
from votes.signals import delete_vote_after_deleting_object
from comments.signals import delete_object_comments_after_deleting
from viewers.signals import delete_object_viewers_after_deleting


post_delete.connect(delete_vote_after_deleting_object, sender=Music)
post_delete.connect(delete_object_comments_after_deleting, sender=Music)
post_delete.connect(delete_object_viewers_after_deleting, sender=Music)


@receiver(post_save, sender=Music)
def notify_music_creation(sender, instance, created, **kwargs):
    
    if created:
        if instance.user == instance.channel.owner:
            send_email.delay(
                template_name="emails/notify_music_creation.html",
                to_email=instance.user.email,
                body={
                    "first_name": instance.user.first_name,
                    "channel_title": instance.title,
                    "channel_token": instance.channel.token,
                    "music_token": instance.token
                }
              )

        else:
            # send email to both admin and owner
            send_email.delay(
                template_name="emails/notify_music_creation.html",
                to_email=instance.user.email,
                body={
                    "first_name": instance.user.first_name,
                    "channel_title": instance.title,
                    "channel_token": instance.channel.token,
                    "music_token": instance.token
                }
              )

            send_email.delay(
                template_name="emails/notify_music_creation.html",
                to_email=instance.channel.owner.email,
                body={
                  "first_name": instance.user.first_name,
                  "channel_title": instance.title,
                  "channel_token": instance.channel.token,
                  "music_token": instance.token
                }
              )
