import pytest
from django.urls import reverse
from rest_framework import status
from contents.models import ContentVisibility
from viewers.models import Viewer


@pytest.mark.django_db
class TestMusicRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, create_music):
        self.music = create_music
        self.url_path = reverse(
            'musics:detail',
            kwargs={
                'channel_token': create_music.channel.token,
                'object_token': create_music.token
            }
        )

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_published_object(self, api_client, create_active_user):
        api_client.force_authenticate(create_active_user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert self.music.visibility == ContentVisibility.PUBLISHED

    def test_retrieve_private_object(self, api_client, create_superuser):
        self.music.visibility = ContentVisibility.PRIVATE
        self.music.save()
        api_client.force_authenticate(create_superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.music.visibility == ContentVisibility.PRIVATE

    def test_retrieve_private_by_admins(self, api_client, create_channel_admin):
        self.music.visibility = ContentVisibility.PRIVATE
        self.music.save()
        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert self.music.visibility == ContentVisibility.PRIVATE

    def test_retrieve_inc_viewers(self, api_client, create_channel_admin):
        """
        Inc the viewer of an object after retrieving
        """
        self.music.visibility = ContentVisibility.PRIVATE
        self.music.save()
        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert Viewer.objects.get_count(
            channel=self.music.channel,
            content_object=self.music
        ) == 1
        assert self.music.visibility == ContentVisibility.PRIVATE
