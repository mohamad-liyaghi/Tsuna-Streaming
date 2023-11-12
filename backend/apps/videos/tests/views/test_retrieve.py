import pytest
from django.urls import reverse
from rest_framework import status
from contents.models import ContentVisibility
from viewers.models import Viewer


@pytest.mark.django_db
class TestVideoRetrieveView:
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

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_published_object(self, api_client, user):
        api_client.force_authenticate(user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert self.video.visibility == ContentVisibility.PUBLISHED

    def test_retrieve_private_object(self, api_client, superuser):
        self.video.visibility = ContentVisibility.PRIVATE
        self.video.save()
        api_client.force_authenticate(superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.video.visibility == ContentVisibility.PRIVATE

    def test_retrieve_private_by_admins(self, api_client, channel_admin):
        self.video.visibility = ContentVisibility.PRIVATE
        self.video.save()
        api_client.force_authenticate(channel_admin.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert self.video.visibility == ContentVisibility.PRIVATE

    def test_retrieve_inc_viewers(self, api_client, channel_admin):
        self.video.visibility = ContentVisibility.PRIVATE
        self.video.save()
        api_client.force_authenticate(channel_admin.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert (
            Viewer.objects.get_count(
                channel=self.video.channel, content_object=self.video
            )
            != 0
        )
        assert self.video.visibility == ContentVisibility.PRIVATE
