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

    def test_unauthorized(self, create_channel, api_client):
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": create_channel.token})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_found(self, api_client, create_unique_uuid, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": create_unique_uuid})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_subscribed_channel_owner(self, create_channel, api_client):
        api_client.force_authenticate(user=create_channel.owner)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": create_channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_db_subscriber(
        self, create_channel, create_subscriber, api_client
    ):
        api_client.force_authenticate(user=create_subscriber.user)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": create_channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_in_cache(self, create_cached_subscriber, api_client):
        user = Account.objects.get(id=create_cached_subscriber["user"])
        channel = Channel.objects.get(id=create_cached_subscriber["channel"])

        api_client.force_authenticate(user=user)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_not_subscribed(
        self, create_channel, create_superuser, api_client
    ):
        api_client.force_authenticate(create_superuser)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": create_channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is False

    def test_subscriber_removed_from_cache(self, create_cached_subscriber, api_client):
        account = Account.objects.get(id=create_cached_subscriber["user"])
        channel = Channel.objects.get(id=create_cached_subscriber["channel"])
        api_client.force_authenticate(account)
        ChannelSubscriber.objects.delete_in_cache(user=account, channel=channel)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is False
