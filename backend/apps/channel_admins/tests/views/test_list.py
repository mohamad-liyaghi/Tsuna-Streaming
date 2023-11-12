import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
class TestAdminListView:
    def setup(self):
        self.url_path = "channel_admins:admin_list_create"

    def test_get_list_unauthorized(self, api_client, channel):
        response = api_client.get(
            reverse(self.url_path, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_invalid_channel(self, create_unique_uuid, api_client):
        response = api_client.get(
            reverse(self.url_path, kwargs={"channel_token": create_unique_uuid})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_by_channel_owner(self, api_client, channel):
        api_client.force_authenticate(user=channel.owner)
        response = api_client.get(
            reverse(self.url_path, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_admin(self, api_client, channel_admin):
        api_client.force_authenticate(user=channel_admin.user)
        response = api_client.get(
            reverse(
                self.url_path,
                kwargs={"channel_token": channel_admin.channel.token},
            )
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_not_admin(self, api_client, channel, another_user):
        api_client.force_authenticate(user=another_user)
        response = api_client.get(
            reverse(self.url_path, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
