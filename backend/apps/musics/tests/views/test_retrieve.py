import pytest
from django.urls import reverse
from rest_framework import status
from contents.models import ContentVisibility
from viewers.models import Viewer


@pytest.mark.django_db
class TestMusicRetrieveView:
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

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_published_object(self, api_client, another_user):
        api_client.force_authenticate(another_user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert self.music.visibility == ContentVisibility.PUBLISHED

    def test_retrieve_private_object(self, api_client, superuser):
        self.music.visibility = ContentVisibility.PRIVATE
        self.music.save()
        api_client.force_authenticate(superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.music.visibility == ContentVisibility.PRIVATE

    def test_retrieve_private_by_admins(self, api_client, channel_admin):
        self.music.visibility = ContentVisibility.PRIVATE
        self.music.save()
        api_client.force_authenticate(channel_admin.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert self.music.visibility == ContentVisibility.PRIVATE

    def test_retrieve_inc_viewers(self, api_client, channel_admin):
        """
        Inc the viewer of an object after retrieving
        """
        self.music.visibility = ContentVisibility.PRIVATE
        self.music.save()
        api_client.force_authenticate(channel_admin.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert (
            Viewer.objects.get_count(
                channel=self.music.channel, content_object=self.music
            )
            != 0
        )
        assert self.music.visibility == ContentVisibility.PRIVATE
