from django.urls import reverse
from rest_framework import status
import pytest
from channel_subscribers.models import ChannelSubscriber


@pytest.mark.django_db
class TestSubscriberView:
    def setup(self):
        self.url_name = 'channel_subscribers:subscriber_status'

    def test_unauthorized(self, create_channel, api_client):
        response = api_client.get(
            reverse(
                self.url_name, kwargs={'channel_token': create_channel.token}
            )
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_found(self, api_client, create_unique_uuid, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.get(
            reverse(self.url_name, kwargs={'channel_token': create_unique_uuid})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_subscribed_channel_owner(self, create_channel, api_client):
        api_client.force_authenticate(user=create_channel.owner)
        response = api_client.get(
            reverse(
                self.url_name, kwargs={'channel_token': create_channel.token}
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_db_subscriber(
            self,
            create_channel,
            create_subscriber,
            api_client
    ):
        api_client.force_authenticate(user=create_subscriber.user)
        response = api_client.get(
            reverse(
                self.url_name, kwargs={'channel_token': create_channel.token}
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_in_cache(self, create_cached_subscriber, api_client):
        api_client.force_authenticate(user=create_cached_subscriber['user'])
        response = api_client.get(
            reverse(
                self.url_name, kwargs={
                    'channel_token': create_cached_subscriber['channel'].token
                }
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is True

    def test_subscriber_not_subscribed(
            self,
            create_channel,
            create_superuser,
            api_client
    ):
        api_client.force_authenticate(create_superuser)
        response = api_client.get(
            reverse(
                self.url_name, kwargs={'channel_token': create_channel.token}
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data is False


# TODO: Unsubscribe in cache
