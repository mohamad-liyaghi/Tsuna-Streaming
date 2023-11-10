import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestChannelList:
    def setup(self):
        self.url = reverse("channels:list-create")

    def test_get_unauthorized(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_by_superuser(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_normal_user(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_premium_user(self, api_client, premium_user):
        api_client.force_authenticate(user=premium_user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
