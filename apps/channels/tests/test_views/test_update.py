import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestChannelUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, create_channel):
        self.url_name = "channels:channel_detail"
        self.channel = create_channel
        self.data = {
            "title": "test",
        }

    def test_update_unauthorized(self, api_client):
        url = reverse(self.url_name, kwargs={"channel_token": self.channel.token})
        response = api_client.put(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_channel_owner(self, api_client):
        url = reverse(
            self.url_name, kwargs={"channel_token": self.channel.token}
        )
        api_client.force_authenticate(user=self.channel.owner)
        response = api_client.put(url, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_others(self, api_client, create_superuser):
        url = reverse(
            self.url_name, kwargs={"channel_token": self.channel.token}
        )
        api_client.force_authenticate(user=create_superuser)
        response = api_client.put(url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_not_found(
            self, api_client, create_unique_uuid, create_active_user
    ):
        url = reverse(
            self.url_name, kwargs={"channel_token": create_unique_uuid}
        )
        api_client.force_authenticate(user=create_active_user)
        response = api_client.put(url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

# TODO: Update by channel admins