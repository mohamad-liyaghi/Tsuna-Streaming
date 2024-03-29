import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestChannelRetrieve:
    @pytest.fixture(autouse=True)
    def setup(self, channel):
        self.url_name = "channels:channel_detail"
        self.channel = channel

    def test_retrieve_unauthorized(self, api_client):
        url = reverse(self.url_name, kwargs={"channel_token": self.channel.token})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_by_superuser(self, api_client, superuser):
        url = reverse(self.url_name, kwargs={"channel_token": self.channel.token})
        api_client.force_authenticate(user=superuser)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_normal_user(self, api_client, user):
        url = reverse(self.url_name, kwargs={"channel_token": self.channel.token})
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_premium_user(self, api_client, premium_user):
        url = reverse(self.url_name, kwargs={"channel_token": self.channel.token})
        api_client.force_authenticate(user=premium_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_not_fount(self, api_client, create_unique_uuid, user):
        url = reverse(self.url_name, kwargs={"channel_token": create_unique_uuid})
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
