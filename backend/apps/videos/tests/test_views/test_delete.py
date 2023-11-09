import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestVideoDeleteView:
    @pytest.fixture(autouse=True)
    def setup(self, create_video):
        self.video = create_video
        self.url_path = reverse(
            "videos:detail",
            kwargs={
                "channel_token": create_video.channel.token,
                "object_token": create_video.token,
            },
        )

    def test_delete_unauthorized(self, api_client):
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_non_admin(self, api_client, create_superuser):
        api_client.force_authenticate(create_superuser)
        response = api_client.delete(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_admin_no_permission(self, create_channel_admin, api_client):
        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.delete(self.url_path)
        assert not create_channel_admin.permissions.can_delete_object
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_admin_with_permission(self, create_channel_admin, api_client):
        create_channel_admin.permissions.can_delete_object = True
        create_channel_admin.permissions.save()
        create_channel_admin.permissions.refresh_from_db()

        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.delete(self.url_path)
        assert create_channel_admin.permissions.can_delete_object
        assert response.status_code == status.HTTP_204_NO_CONTENT
