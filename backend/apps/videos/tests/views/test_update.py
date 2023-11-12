import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestVideoUpdateView:
    @pytest.fixture(autouse=True)
    def setup(self, video):
        self.video = video
        self.url_path = reverse(
            "videos:detail",
            kwargs={
                "channel_token": video.channel.token,
                "object_token": video.token,
            },
        )
        self.data = {
            "title": "test updated title",
            "description": "test updated description",
        }

    def test_update_unauthorized(self, api_client):
        response = api_client.put(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_non_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.put(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_admin_no_permission(self, channel_admin, api_client):
        api_client.force_authenticate(channel_admin.user)
        response = api_client.put(self.url_path, self.data, format="json")
        assert not channel_admin.permissions.can_edit_object
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_by_admin_with_permission(self, channel_admin, api_client):
        channel_admin.permissions.can_edit_object = True
        channel_admin.permissions.save()
        channel_admin.permissions.refresh_from_db()

        api_client.force_authenticate(channel_admin.user)
        response = api_client.put(self.url_path, self.data, format="json")
        assert channel_admin.permissions.can_edit_object
        assert response.status_code == status.HTTP_200_OK
