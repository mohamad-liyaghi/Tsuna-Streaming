from accounts.models import Account, Subscription, Plan
import pytest

@pytest.mark.django_db
class TestSubscriptionModel:
    
    def setup(self):
        self.premium_user = Account.objects.create_user(email="user1@simple.com", password="1234USERnormal")
        self.plan = Plan.objects.create(title="plan", active_months=1)
        self.subscription = Subscription.objects.create(user=self.premium_user, plan=self.plan)
        self.normal_user = Account.objects.create_user(email="user2@simple.com", password="1234USERnormal")
    
    def test_user_role_after_creating_subscription(self):
        assert self.premium_user.role == "p"
        assert self.normal_user.role == "n"

    def test_user_role_after_deleting_plan(self):
        assert self.premium_user.role == "p"
        self.subscription.delete()
        assert self.premium_user.role == "n"
    
    
    


        