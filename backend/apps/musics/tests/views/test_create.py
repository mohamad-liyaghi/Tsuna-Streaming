import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from contents.models import ContentVisibility


@pytest.mark.django_db
class TestMusicCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, music, create_file):
        self.music = music
        self.url_path = reverse(
            "musics:list_create", kwargs={"channel_token": music.channel.token}
        )
        self.data = {
            "title": "fake title",
            "description": "fake description",
            "file": SimpleUploadedFile(
                name=create_file.name, content=b"test", content_type="audio/mpeg"
            ),
            "allow_comment": False,
            "visibility": ContentVisibility.PUBLISHED,
        }

    def test_create_unauthenticated(self, api_client):
        response = api_client.post(self.url_path, data=self.data, format="multipart")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_no_permission(self, channel_admin, api_client):
        api_client.force_authenticate(channel_admin.user)
        response = api_client.post(self.url_path, data=self.data, format="multipart")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not channel_admin.permissions.can_add_object

    def test_create_by_channel_owner(self, api_client):
        api_client.force_authenticate(self.music.channel.owner)
        response = api_client.post(self.url_path, data=self.data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_accessed_admin(self, api_client, channel_admin):
        channel_admin.permissions.can_add_object = True
        channel_admin.permissions.save()

        api_client.force_authenticate(channel_admin.user)
        response = api_client.post(self.url_path, data=self.data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert channel_admin.permissions.can_add_object
