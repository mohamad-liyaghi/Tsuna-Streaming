import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMembershipDeleteView:
    @pytest.fixture(autouse=True)
    def setup(self, membership):
        self.url_name = "memberships:membership_detail"
        self.membership = membership

    def test_delete_unauthorized(self, api_client):
        response = api_client.delete(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_superuser(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_premium_user(self, api_client, premium_user):
        api_client.force_authenticate(premium_user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_normal_user(self, api_client, user):
        api_client.force_authenticate(user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_not_found(self, superuser, api_client, create_unique_uuid):
        api_client.force_authenticate(superuser)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"membership_token": create_unique_uuid})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_in_use_plan(self, api_client, subscription, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={"membership_token": subscription.membership.token},
            )
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
