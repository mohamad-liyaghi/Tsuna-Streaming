from templated_mail.mail import BaseEmailMessage
from celery import shared_task

@shared_task
def send_email(email, first_name, token):
    BaseEmailMessage(template_name="emails/verification.html", 
                context={"first_name" : first_name, "token" : token}).send(to=[email])
