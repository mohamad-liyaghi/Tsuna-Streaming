from django.conf import settings
from templated_mail.mail import BaseEmailMessage
from celery import shared_task


@shared_task
def send_email(
        template_name: str, to_email: str, body: dict
):
    """
    Send an email to the given user
    :param template_name: The name of the template to send
    :param to_email: The email address to send to
    :param body: The context to send to the template
    """

    # Set the domain for the email
    body.setdefault("domain", settings.DOMAIN)

    # Send email to user
    email = BaseEmailMessage(template_name=template_name, context=body)
    email.send(to=[to_email])
