import pytest
from rest_framework import status
from django.urls import reverse
from channel_admins.models import ChannelAdmin


@pytest.mark.django_db
class TestAdminCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, subscriber):
        self.url_path = "channel_admins:admin_list_create"
        self.data = {
            "user": subscriber.user.token,
        }

    def test_create_unauthorized(self, api_client, channel):
        response = api_client.post(
            reverse(self.url_path, kwargs={"channel_token": channel.token}),
            data=self.data,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_invalid_data(self, api_client, channel):
        api_client.force_authenticate(user=channel.owner)
        response = api_client.post(
            reverse(self.url_path, kwargs={"channel_token": channel.token}),
            data={},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_invalid_channel(self, api_client, create_unique_uuid):
        api_client.force_authenticate(user=create_unique_uuid)
        response = api_client.post(
            reverse(self.url_path, kwargs={"channel_token": create_unique_uuid}),
            data=self.data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_by_channel_owner(self, api_client, channel):
        api_client.force_authenticate(user=channel.owner)
        response = api_client.post(
            reverse(self.url_path, kwargs={"channel_token": channel.token}),
            data=self.data,
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_channel_admin(self, api_client, channel_admin, user):
        # Delete the admin
        ChannelAdmin.objects.get(user=user).delete()
        # Change the user
        self.data["user"] = user.token

        api_client.force_authenticate(user=channel_admin.channel.owner)
        response = api_client.post(
            reverse(
                self.url_path,
                kwargs={"channel_token": channel_admin.channel.token},
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_by_normal_user(self, api_client, superuser, channel):
        api_client.force_authenticate(user=superuser)
        response = api_client.post(
            reverse(self.url_path, kwargs={"channel_token": channel.token}),
            data=self.data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
