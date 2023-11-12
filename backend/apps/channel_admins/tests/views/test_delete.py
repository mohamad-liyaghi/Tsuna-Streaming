import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAdminDelete:
    @pytest.fixture(autouse=True)
    def setup(self, channel_admin):
        self.admin = channel_admin
        self.url_name = "channel_admins:admin_detail"

    def test_delete_unauthorized(self, api_client):
        url = reverse(
            self.url_name,
            kwargs={
                "channel_token": self.admin.channel.token,
                "admin_token": self.admin.token,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_invalid_channel(self, api_client, user, create_unique_uuid):
        api_client.force_authenticate(user=user)
        url = reverse(
            self.url_name,
            kwargs={
                "channel_token": create_unique_uuid,
                "admin_token": self.admin.token,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_invalid_admin(self, api_client, create_unique_uuid):
        api_client.force_authenticate(user=self.admin.channel.owner)
        url = reverse(
            self.url_name,
            kwargs={
                "channel_token": self.admin.channel.token,
                "admin_token": create_unique_uuid,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_by_channel_owner(self, api_client):
        api_client.force_authenticate(user=self.admin.channel.owner)
        url = reverse(
            self.url_name,
            kwargs={
                "channel_token": self.admin.channel.token,
                "admin_token": self.admin.token,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_channel_admin(self, api_client):
        api_client.force_authenticate(user=self.admin.user)
        url = reverse(
            self.url_name,
            kwargs={
                "channel_token": self.admin.channel.token,
                "admin_token": self.admin.token,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_admin_itself(self, api_client):
        api_client.force_authenticate(user=self.admin.user)
        url = reverse(
            self.url_name,
            kwargs={
                "channel_token": self.admin.channel.token,
                "admin_token": self.admin.token,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_not_admin(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        url = reverse(
            self.url_name,
            kwargs={
                "channel_token": self.admin.channel.token,
                "admin_token": self.admin.token,
            },
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
