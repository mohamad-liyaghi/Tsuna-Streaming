from django.urls import reverse
from rest_framework import status
import pytest
from channel_subscribers.models import ChannelSubscriber
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestSubscriberView:
    def setup(self):
        self.url_name = "channel_subscribers:subscriber_status"

    def test_unauthorized(self, channel, api_client):
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_found(self, api_client, create_unique_uuid, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": create_unique_uuid})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_subscribed_channel_owner(self, channel, api_client):
        api_client.force_authenticate(user=channel.owner)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_db_subscriber(self, channel, subscriber, api_client):
        api_client.force_authenticate(user=subscriber.user)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_in_cache(
        self, cached_subscriber, api_client, superuser, channel
    ):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_not_subscribed(self, channel, another_user, api_client):
        api_client.force_authenticate(another_user)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is False

    def test_subscriber_removed_from_cache(
        self, cached_subscriber, api_client, channel, superuser
    ):
        api_client.force_authenticate(superuser)
        ChannelSubscriber.objects.delete_in_cache(user=superuser, channel=channel)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is False
