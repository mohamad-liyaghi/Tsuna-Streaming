import pytest
from django.urls import reverse
from rest_framework import status
from contents.models import ContentVisibility


@pytest.mark.django_db
class TestVideoListView:
    @pytest.fixture(autouse=True)
    def setup(self, video):
        self.video = video
        self.url_path = reverse(
            "videos:list_create", kwargs={"channel_token": video.channel.token}
        )

    def test_get_unauthenticated(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_authenticated(self, api_client, another_user):
        api_client.force_authenticate(user=another_user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_get_private_video_no_param(self, api_client, user):
        api_client.force_authenticate(user=user)
        self.video.visibility = ContentVisibility.PRIVATE
        self.video.save()

        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 0

    def test_get_private_query_param(self, api_client, channel_admin):
        api_client.force_authenticate(user=channel_admin.user)
        self.video.visibility = ContentVisibility.PUBLISHED
        self.video.save()

        response = api_client.get(self.url_path, {"show_private": True})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 1

    def test_get_private_non_admin(self, another_user, api_client):
        api_client.force_authenticate(user=another_user)
        self.video.visibility = ContentVisibility.PUBLISHED
        self.video.save()

        response = api_client.get(self.url_path, {"show_private": True})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_search_invalid_video_title(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.url_path, {"title": "invalid"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 0
