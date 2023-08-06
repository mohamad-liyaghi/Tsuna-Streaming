import pytest
from rest_framework import status
from django.urls import reverse
from channel_admins.models import ChannelAdmin


@pytest.mark.django_db
class TestAdminCreateView:

    @pytest.fixture(autouse=True)
    def setup(self, create_subscriber):
        """
        Create a new subscriber which user can be promoted to admin.
        """
        self.url_path = 'channel_admins:admin_list_create'
        self.data = {
            "user": create_subscriber.user.token,
        }

    def test_create_unauthorized(self, api_client, create_channel):
        response = api_client.post(
            reverse(
                self.url_path,
                kwargs={'channel_token': create_channel.token}
            ),
            data=self.data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_invalid_data(self, api_client, create_channel):
        api_client.force_authenticate(user=create_channel.owner)
        response = api_client.post(
            reverse(
                self.url_path,
                kwargs={'channel_token': create_channel.token}
            ),
            data={}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_invalid_channel(self, api_client, create_unique_uuid):
        api_client.force_authenticate(user=create_unique_uuid)
        response = api_client.post(
            reverse(
                self.url_path,
                kwargs={'channel_token': create_unique_uuid}
            ),
            data=self.data
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_by_channel_owner(self, api_client, create_channel):
        api_client.force_authenticate(user=create_channel.owner)
        response = api_client.post(
            reverse(
                self.url_path,
                kwargs={'channel_token': create_channel.token}
            ),
            data=self.data
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_channel_admin(
            self, api_client,
            create_channel_admin,
            create_active_user
    ):
        # Delete the admin
        ChannelAdmin.objects.get(user=create_active_user).delete()
        # Change the user
        self.data['user'] = create_active_user.token

        api_client.force_authenticate(
            user=create_channel_admin.channel.owner
        )
        response = api_client.post(
            reverse(
                self.url_path,
                kwargs={'channel_token': create_channel_admin.channel.token}
            ),
            data=self.data
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_by_normal_user(
            self, api_client, create_superuser, create_channel
    ):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.post(
            reverse(
                self.url_path,
                kwargs={'channel_token': create_channel.token}
            ),
            data=self.data
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
