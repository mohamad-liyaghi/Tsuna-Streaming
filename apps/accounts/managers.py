from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    
    def create_user(self, email, password, **kwargs):

        email = self.normalize_email(email)

        is_active = False
        user = self.model(email=email, is_active=is_active,
                        role="n", **kwargs)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        email = self.normalize_email(email)

        is_active = True
        user = self.model(email=email, is_active=is_active, is_superuser=True, is_staff=True,
                        role="a", **kwargs)

        user.set_password(password)

        user.save()

        return user
