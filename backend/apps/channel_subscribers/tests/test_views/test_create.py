from django.urls import reverse
from rest_framework import status
import pytest
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestSubscriberCrateView:
    def setup(self):
        self.url_name = "channel_subscribers:create_subscriber"

    def test_unauthorized(self, create_channel, api_client):
        response = api_client.post(
            reverse(self.url_name, kwargs={"channel_token": create_channel.token}), {}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_found(self, api_client, create_unique_uuid, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.post(
            reverse(self.url_name, kwargs={"channel_token": create_unique_uuid}), {}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_subscribe_twice(self, create_subscriber, api_client):
        api_client.force_authenticate(user=create_subscriber.user)
        response = api_client.post(
            reverse(
                self.url_name, kwargs={"channel_token": create_subscriber.channel.token}
            ),
            {},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_subscribe_twice_first_in_cache(self, create_cached_subscriber, api_client):
        api_client.force_authenticate(
            user=Account.objects.get(id=create_cached_subscriber["user"])
        )
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "channel_token": Channel.objects.get(
                        id=create_cached_subscriber["channel"]
                    ).token
                },
            ),
            {},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_subscribe(self, create_channel, create_superuser, api_client):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.post(
            reverse(self.url_name, kwargs={"channel_token": create_channel.token}), {}
        )
        assert response.status_code == status.HTTP_201_CREATED
