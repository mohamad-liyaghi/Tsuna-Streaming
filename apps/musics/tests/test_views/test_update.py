import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMusicUpdateView:

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
        self.data = {
            'title': 'test updated title',
            'description': 'test updated description'
        }

    def test_update_unauthorized(self, api_client):
        response = api_client.put(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_non_admin(self, api_client, create_superuser):
        api_client.force_authenticate(create_superuser)
        response = api_client.put(self.url_path, self.data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_admin_no_permission(self, create_channel_admin, api_client):
        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.put(self.url_path, self.data, format='json')
        assert not create_channel_admin.permissions.can_edit_object
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_by_admin_with_permission(self, create_channel_admin, api_client):
        create_channel_admin.permissions.can_edit_object = True
        create_channel_admin.permissions.save()
        create_channel_admin.permissions.refresh_from_db()

        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.put(self.url_path, self.data, format='json')
        assert create_channel_admin.permissions.can_edit_object
        assert response.status_code == status.HTTP_200_OK

    def test_update_invalid_data(self, create_channel_admin, api_client):
        create_channel_admin.permissions.can_edit_object = True
        create_channel_admin.permissions.save()
        create_channel_admin.permissions.refresh_from_db()

        api_client.force_authenticate(create_channel_admin.user)
        response = api_client.put(self.url_path, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
