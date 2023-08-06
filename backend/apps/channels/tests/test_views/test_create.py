import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestChannelCreate:
    def setup(self):
        self.url = reverse("channels:list-create")
        self.data = {
            "title": "test channel",
            "description": "test description",
        }

    def test_create_unauthorized(self, api_client):
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_by_superuser(self, api_client, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_normal_user(self, api_client, create_active_user):
        api_client.force_authenticate(user=create_active_user)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_premium_user(self, api_client, create_premium_user):
        api_client.force_authenticate(user=create_premium_user)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_normal_user_more_than_5(
            self, api_client, create_active_user
    ):
        api_client.force_authenticate(user=create_active_user)
        for _ in range(6):
            api_client.post(self.url, self.data, format="json")
        assert create_active_user.channels.count() == 5
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_by_premium_user_more_than_10(
            self, api_client, create_premium_user
    ):
        api_client.force_authenticate(user=create_premium_user)
        for _ in range(11):
            api_client.post(self.url, self.data, format="json")
        assert create_premium_user.channels.count() == 10
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
