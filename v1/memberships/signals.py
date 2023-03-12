from django.db.models.signals import pre_save
from memberships.models import Membership
from v1.core.receivers import create_token_after_creating_object


# Create unique token for each Membership 
pre_save.connect(create_token_after_creating_object, sender=Membership)
