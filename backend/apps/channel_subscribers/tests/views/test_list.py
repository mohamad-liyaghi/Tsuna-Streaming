from django.urls import reverse
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestSubscriberListView:
    def setup(self):
        self.url_name = "channel_subscribers:subscriber_list"

    def test_unauthorized(self, channel, api_client):
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": channel.token})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_not_found(self, api_client, create_unique_uuid):
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": create_unique_uuid})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_list(self, subscriber, api_client):
        api_client.force_authenticate(user=subscriber.user)
        response = api_client.get(
            reverse(self.url_name, kwargs={"channel_token": subscriber.channel.token})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
