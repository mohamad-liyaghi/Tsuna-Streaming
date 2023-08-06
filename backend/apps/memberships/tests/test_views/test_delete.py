import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMembershipDelete:

    @pytest.fixture(autouse=True)
    def setup(self, create_membership):
        self.url_name = "memberships:membership_detail"
        self.membership = create_membership

    def test_delete_unauthorized(self, api_client):
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            )
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_superuser(self, api_client, create_superuser):
        api_client.force_authenticate(create_superuser)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            )
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_premium_user(self, api_client, create_premium_user):
        api_client.force_authenticate(create_premium_user)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_normal_user(self, api_client, create_active_user):
        api_client.force_authenticate(create_active_user)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_not_found(
            self, create_superuser, api_client, create_unique_uuid
    ):
        api_client.force_authenticate(create_superuser)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={"membership_token": create_unique_uuid}
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_in_use_plan(self, api_client, create_subscription, create_superuser):
        api_client.force_authenticate(create_superuser)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={"membership_token": create_subscription.membership.token}
            )
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
