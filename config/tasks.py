from django.conf import settings
from templated_mail.mail import BaseEmailMessage
from celery import shared_task


@shared_task
def send_email(template_name, email, **kwargs):
    '''This functions handels the notifications that should be sent by email'''

    # Add the domain into kwargs that is saved in settings
    kwargs.setdefault("domain", settings.DOMAIN)

    # Send the actual email to the given user
    BaseEmailMessage(
            template_name=template_name,
            context={"kwargs" : kwargs}
            ) .send(to=[email]
        )