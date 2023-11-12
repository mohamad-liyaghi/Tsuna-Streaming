import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMusicDeleteView:
    @pytest.fixture(autouse=True)
    def setup(self, music):
        self.music = music
        self.url_path = reverse(
            "musics:detail",
            kwargs={
                "channel_token": music.channel.token,
                "object_token": music.token,
            },
        )

    def test_delete_unauthorized(self, api_client):
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_non_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_admin_no_permission(self, channel_admin, api_client):
        api_client.force_authenticate(channel_admin.user)
        response = api_client.delete(self.url_path)
        assert not channel_admin.permissions.can_delete_object
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_admin_with_permission(self, channel_admin, api_client):
        channel_admin.permissions.can_delete_object = True
        channel_admin.permissions.save()
        channel_admin.permissions.refresh_from_db()

        api_client.force_authenticate(channel_admin.user)
        response = api_client.delete(self.url_path)
        assert channel_admin.permissions.can_delete_object
        assert response.status_code == status.HTTP_204_NO_CONTENT
