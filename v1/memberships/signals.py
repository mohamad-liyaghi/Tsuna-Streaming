from django.db.models.signals import pre_save
from memberships.models import Membership, Subscription
from v1.core.receivers import create_token_after_creating_object

# create unique token for each object
pre_save.connect(create_token_after_creating_object, sender=Membership)
pre_save.connect(create_token_after_creating_object, sender=Subscription)
