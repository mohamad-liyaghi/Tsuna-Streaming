from django.contrib.auth.models import BaseUserManager
from accounts.tasks import send_email
from django.db import models
from django.utils import timezone

import datetime

class AccountManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        email = self.normalize_email(email)

        try: 
            kwargs["bio"]
        except:
            kwargs["bio"] = "Hey there, i am using tsuna streaming."

        is_active = False
        user = self.model(email=email, is_active=is_active,
                        role="n", **kwargs)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        email = self.normalize_email(email)

        try: 
            kwargs["bio"]
        except:
            kwargs["bio"] = "Hey there, i am using tsuna streaming."
        is_active = True
        user = self.model(email=email, is_active=is_active, is_superuser=True, is_staff=True,
                        role="a", **kwargs)

        user.set_password(password)

        user.save()

        return user


class TokenManager(models.Manager):

    def create(self, user, **kwargs):

        token = self.model(user=user, **kwargs)
        token.save()

        send_email.delay("verification", email=user.email, first_name=user.first_name, 
                                        user_id = user.user_id, token=token.token)

        return token


class SubscriptionManager(models.Manager):
    def create(self, **kwargs):

        if kwargs["user"].role == "p":
            raise ValueError('User is already a premium user.')

        plan_active_months = kwargs["plan"].active_months

        finish_date = timezone.now() + datetime.timedelta(plan_active_months * 30)
        
        subscription = self.model(finish_date=finish_date, **kwargs)
        subscription.save()

        #TODO send email to notify user
        
        # update user to premium
        subscription.user.role = "p"
        subscription.user.save()

        return subscription
        