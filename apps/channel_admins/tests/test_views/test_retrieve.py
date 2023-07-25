import pytest
from django.urls import reverse
from rest_framework import status
from channel_admins.models import ChannelAdmin


@pytest.mark.django_db
class TestAdminRetrieve:
    @pytest.fixture(autouse=True)
    def setup(self, create_channel_admin):
        self.admin = create_channel_admin
        self.url_name = 'channel_admins:admin_detail'

    def test_retrieve_unauthorized(self, api_client):
        url = reverse(self.url_name, kwargs={
            'channel_token': self.admin.channel.token,
            'admin_token': self.admin.token
        })
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_invalid_channel(
            self, api_client, create_active_user, create_unique_uuid
    ):
        api_client.force_authenticate(user=create_active_user)
        url = reverse(self.url_name, kwargs={
            'channel_token': create_unique_uuid,
            'admin_token': self.admin.token
        })
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_invalid_admin(
            self, api_client, create_unique_uuid
    ):
        api_client.force_authenticate(user=self.admin.user)
        url = reverse(self.url_name, kwargs={
            'channel_token': self.admin.channel.token,
            'admin_token': create_unique_uuid
        })
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_by_admin(self, api_client):
        api_client.force_authenticate(user=self.admin.user)
        url = reverse(self.url_name, kwargs={
            'channel_token': self.admin.channel.token,
            'admin_token': self.admin.token
        })
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_not_admin(self, api_client, create_active_user):
        # Delete the users admin instance
        ChannelAdmin.objects.filter(user=create_active_user).delete()

        api_client.force_authenticate(user=create_active_user)
        url = reverse(self.url_name, kwargs={
            'channel_token': self.admin.channel.token,
            'admin_token': self.admin.token
        })
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
