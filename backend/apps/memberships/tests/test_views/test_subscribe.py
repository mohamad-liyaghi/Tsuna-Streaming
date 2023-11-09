import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMembershipSubscribe:
    @pytest.fixture(autouse=True)
    def setup(self, create_membership):
        self.url_name = "memberships:membership_subscribe"
        self.membership = create_membership

    def test_subscribe_unauthorized(self, api_client):
        response = api_client.post(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_subscribe_by_superuser(self, api_client, create_superuser):
        api_client.force_authenticate(create_superuser)
        response = api_client.post(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_subscribe_by_premium_user(self, api_client, create_premium_user):
        api_client.force_authenticate(create_premium_user)
        response = api_client.post(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_subscribe_by_normal_user(self, api_client, create_active_user):
        api_client.force_authenticate(create_active_user)
        response = api_client.post(
            reverse(self.url_name, kwargs={"membership_token": self.membership.token})
        )
        assert response.status_code == status.HTTP_201_CREATED
        create_active_user.refresh_from_db()
        assert create_active_user.is_premium()

    def test_subscribe_not_found(
        self, create_active_user, api_client, create_unique_uuid
    ):
        api_client.force_authenticate(create_active_user)
        response = api_client.post(
            reverse(self.url_name, kwargs={"membership_token": create_unique_uuid})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
