from django.urls import reverse
from rest_framework import status
import pytest
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestSubscriberCrateView:
    def setup(self):
        self.url_name = "channel_subscribers:create_subscriber"

    def test_subscribe_unauthorized_fails(self, channel, api_client):
        response = api_client.post(
            reverse(self.url_name, kwargs={"channel_token": channel.token}), {}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_subscribe_not_found(self, api_client, create_unique_uuid, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.post(
            reverse(self.url_name, kwargs={"channel_token": create_unique_uuid}), {}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_subscribe_twice_fails(self, subscriber, api_client):
        api_client.force_authenticate(user=subscriber.user)
        response = api_client.post(
            reverse(self.url_name, kwargs={"channel_token": subscriber.channel.token}),
            {},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_subscribe_twice_first_in_cache(
        self, cached_subscriber, channel, superuser, api_client
    ):
        api_client.force_authenticate(user=superuser)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={"channel_token": channel.token},
            ),
            {},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_subscribe(self, channel, another_user, api_client):
        api_client.force_authenticate(user=another_user)
        response = api_client.post(
            reverse(self.url_name, kwargs={"channel_token": channel.token}), {}
        )
        assert response.status_code == status.HTTP_201_CREATED
