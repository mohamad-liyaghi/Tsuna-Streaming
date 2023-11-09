import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from contents.models import ContentVisibility


@pytest.mark.django_db
class TestMusicCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, create_music, create_file):
        self.music = create_music
        self.url_path = reverse(
            "musics:list_create", kwargs={"channel_token": create_music.channel.token}
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

    def test_create_no_permission(self, create_channel_admin, api_client):
        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.post(self.url_path, data=self.data, format="multipart")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not create_channel_admin.permissions.can_add_object

    def test_create_by_channel_owner(self, api_client):
        api_client.force_authenticate(self.music.channel.owner)
        response = api_client.post(self.url_path, data=self.data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_accessed_admin(self, api_client, create_channel_admin):
        create_channel_admin.permissions.can_add_object = True
        create_channel_admin.permissions.save()

        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.post(self.url_path, data=self.data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert create_channel_admin.permissions.can_add_object
