from accounts.models import Account
from memberships.models import Membership, Subscription
from memberships.exceptions import MembershipInUserError
from django.utils import timezone
import datetime
import pytest


@pytest.mark.django_db
class TestMembershipModel:
    def create_user(self):
        self.normal_user = Account.objects.create_user(email="user2@simple.com", password="1234USERnormal")
        self.premium_user = Account.objects.create_user(email="user1@simple.com", password="1234USERnormal")

    def setup(self):
        self.create_user()
        self.membership = Membership.objects.create(title="membership", active_months=1)
        # make the user premium
        self.subscription = Subscription.objects.create(user=self.premium_user, membership=self.membership)
        
    
    def test_user_role_after_creating_subscription(self):
        assert self.premium_user.role == "p"
        assert self.normal_user.role == "n"


    def test_user_active_subscription(self):
        assert self.premium_user.subscription.first().membership.title == self.membership.title

    def test_user_role_after_deleting_membership(self):
        assert self.premium_user.role == "p"
        self.subscription.delete()
        assert self.premium_user.role == "n"
    

    def test_subscription_finish_date(self):
        now = timezone.now()   
        one_month_from_now = now + datetime.timedelta(self.membership.active_months * 30)
        assert self.subscription.finish_date.strftime("%m/%d/%Y %H:%M:%S") == one_month_from_now.strftime("%m/%d/%Y %H:%M:%S")

    def test_raise_subscription_deletion(self):
        '''A membership that is in use by subscription can not be deleted.'''

        with pytest.raises(MembershipInUserError):
            self.membership.delete()
        
    def test_change_user_role_after_deleting_sub(self):
        self.subscription.delete()
        assert self.premium_user.role == 'n'
