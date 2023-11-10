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

    def test_create_unauthorized_fails(self, api_client):
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_by_superuser(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_normal_user(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_premium_user(self, api_client, premium_user):
        api_client.force_authenticate(user=premium_user)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_by_normal_user_more_than_5(self, api_client, another_user):
        api_client.force_authenticate(user=another_user)
        for _ in range(6):
            api_client.post(self.url, self.data, format="json")
        assert another_user.channels.count() == 5
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_by_premium_user_more_than_10(self, api_client, premium_user):
        api_client.force_authenticate(user=premium_user)
        for _ in range(11):
            api_client.post(self.url, self.data, format="json")
        assert premium_user.channels.count() == 10
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
