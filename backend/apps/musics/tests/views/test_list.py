import pytest
from django.urls import reverse
from rest_framework import status
from contents.models import ContentVisibility


@pytest.mark.django_db
class TestMusicListView:
    @pytest.fixture(autouse=True)
    def setup(self, music):
        self.music = music
        self.url_path = reverse(
            "musics:list_create", kwargs={"channel_token": music.channel.token}
        )

    def test_get_unauthenticated(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_authenticated(self, api_client, another_user):
        api_client.force_authenticate(user=another_user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_get_private_music_no_param(self, api_client, another_user):
        api_client.force_authenticate(user=another_user)
        self.music.visibility = ContentVisibility.PRIVATE
        self.music.save()

        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 0

    def test_get_private_query_param(self, api_client, channel_admin):
        api_client.force_authenticate(user=channel_admin.user)
        self.music.visibility = ContentVisibility.PUBLISHED
        self.music.save()

        response = api_client.get(self.url_path, {"show_private": True})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 1

    def test_get_private_non_admin(self, another_user, api_client):
        api_client.force_authenticate(user=another_user)
        self.music.visibility = ContentVisibility.PUBLISHED
        self.music.save()

        response = api_client.get(self.url_path, {"show_private": True})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_search_invalid_music_title(self, api_client, another_user):
        api_client.force_authenticate(user=another_user)
        response = api_client.get(self.url_path, {"title": "invalid"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 0
