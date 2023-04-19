from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.core.tasks import send_email
from musics.models import Music
from votes.signals import delete_object_votes_after_deleting
from comments.signals import delete_object_comments_after_deleting
from viewers.signals import delete_object_viewers_after_deleting


post_delete.connect(delete_object_votes_after_deleting, sender=Music)
post_delete.connect(delete_object_comments_after_deleting, sender=Music)
post_delete.connect(delete_object_viewers_after_deleting, sender=Music)


@receiver(post_save, sender=Music)
def notify_music_creation(sender, instance, created, **kwargs):
    
    if created:
        print(instance.token)
            
        if instance.user == instance.channel.owner:
            send_email(template_name="emails/notify_music_creation.html", first_name=instance.user.first_name,
                        email=instance.user.email, channel_title=instance.title, channel_token=instance.channel.token,
                          music_token=instance.token)

        else:
            # send email to both admin and owner
            send_email(template_name="emails/notify_music_creation.html", first_name=instance.user.first_name,
                        email=instance.user.email, channel_title=instance.title, channel_token=instance.channel.token,
                        music_token=instance.token)

            send_email(template_name="emails/notify_music_creation.html", first_name=instance.user.first_name,
                        email=instance.channel.owner.email, channel_title=instance.title, channel_token=instance.channel.token,
                          music_token=instance.token)

