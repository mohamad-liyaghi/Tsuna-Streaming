from django.urls import reverse
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestRetrieveProfileView:
    def setup(self):
        self.url_path = "accounts:profile"

    def test_retrieve_profile_unauthorized_fails(self, user, api_client):
        url = reverse(self.url_path, kwargs={"user_token": user.token})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_profile(self, user, api_client):
        api_client.force_authenticate(user=user)
        url = reverse(self.url_path, kwargs={"user_token": user.token})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_inactive_user_fails(self, user, api_client, inactive_user):
        api_client.force_authenticate(user=user)
        url = reverse(self.url_path, kwargs={"user_token": inactive_user.token})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_others_profile(self, user, api_client, superuser):
        api_client.force_authenticate(user=user)
        url = reverse(self.url_path, kwargs={"user_token": superuser.token})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_non_exist_profile_fails(
        self, superuser, api_client, create_unique_uuid
    ):
        api_client.force_authenticate(user=superuser)
        url = reverse(self.url_path, kwargs={"user_token": create_unique_uuid})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
