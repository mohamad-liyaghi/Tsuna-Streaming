from django.contrib.auth.models import BaseUserManager
import random

class AccountManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        email = self.normalize_email(email)

        try: 
            kwargs["bio"]
        except:
            kwargs["bio"] = "Hey there, i am using tsuna streaming."

        user_id = random.randint(0, 999999999999999)
        is_active = False
        user = self.model(email=email, user_id=user_id, is_active=is_active,
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

        user_id = random.randint(0, 999999999999999)
        is_active = True
        user = self.model(email=email, user_id=user_id, is_active=is_active, is_superuser=True, is_staff=True,
                        role="a", **kwargs)

        user.set_password(password)

        user.save()

        return user