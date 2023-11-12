from django.urls import reverse
from rest_framework import status
import pytest
from channel_subscribers.models import ChannelSubscriber
from channels.models import Channel
from accounts.models import Account


@pytest.mark.django_db
class TestSubscriberDeleteView:
    def setup(self):
        self.url_name = "channel_subscribers:delete_subscriber"

    def test_unsubscribe_unauthorized_fails(self, channel, api_client):
        response = api_client.delete(
            reverse(self.url_name, kwargs={"channel_token": channel.token}),
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unsubscribe_not_found(self, api_client, create_unique_uuid, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"channel_token": create_unique_uuid}),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_unsubscribed(self, api_client, channel, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"channel_token": channel.token}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not ChannelSubscriber.objects.get_from_cache(
            channel=channel, user=superuser
        )

    def test_delete_from_db(self, subscriber, api_client):
        api_client.force_authenticate(subscriber.user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"channel_token": subscriber.channel.token}),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ChannelSubscriber.objects.get_from_cache(
            channel=subscriber.channel, user=subscriber.user
        )

    def test_delete_from_cache(self, cached_subscriber, api_client):
        user = Account.objects.get(id=cached_subscriber["user"])
        channel = Channel.objects.get(id=cached_subscriber["channel"])
        api_client.force_authenticate(user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={"channel_token": channel.token}),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
