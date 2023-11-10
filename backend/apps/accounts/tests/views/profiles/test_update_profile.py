import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUpdateProfileView:
    def setup(self):
        self.url_path = "accounts:profile"
        self.data = {
            "first_name": "Updated first name",
        }

    def test_update_profile_unauthorized(self, user, api_client):
        url = reverse(self.url_path, kwargs={"user_token": user.token})
        response = api_client.put(url, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, user, api_client):
        api_client.force_authenticate(user=user)
        url = reverse(self.url_path, kwargs={"user_token": user.token})
        response = api_client.put(url, self.data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_update_profile_invalid_data(self, user, api_client):
        api_client.force_authenticate(user=user)
        url = reverse(self.url_path, kwargs={"user_token": user.token})
        response = api_client.put(url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_other_profile(self, user, superuser, api_client):
        api_client.force_authenticate(user=user)
        url = reverse(self.url_path, kwargs={"user_token": superuser.token})
        response = api_client.put(url, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_non_existing_profile(self, user, api_client, create_unique_uuid):
        api_client.force_authenticate(user=user)
        url = reverse(self.url_path, kwargs={"user_token": create_unique_uuid})
        response = api_client.put(url, {}, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
