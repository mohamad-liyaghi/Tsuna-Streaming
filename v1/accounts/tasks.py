from templated_mail.mail import BaseEmailMessage
from celery import shared_task


@shared_task
def send_email(type, **kwargs):
    '''This email task can be used for email verification and other purposes'''

    if type == "verification":
        
        first_name = kwargs.get("first_name")    
        user_id = kwargs.get("user_id")    
        token = kwargs.get("token")    
        email = kwargs.get("email")

        BaseEmailMessage(template_name="emails/verification.html", 
                    context={"first_name" : first_name, "user_id" : user_id,
                                 "token" : token}).send(to=[email])
