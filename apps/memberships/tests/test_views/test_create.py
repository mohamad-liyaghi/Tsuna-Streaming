import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMembershipCreate:
    def setup(self):
        self.url = reverse("memberships:membership")
        self.data = {
            "title": "Test Membership",
            "description": "Test Membership Description",
            "price": 100,
            "active_months": 6,
            "is_available": True,
        }

    def test_get_unauthorized(self, api_client):
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_by_superuser(self, create_superuser, api_client):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_by_premium_user(self, create_premium_user, api_client):
        api_client.force_authenticate(user=create_premium_user)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_by_normal_user(self, create_active_user, api_client):
        api_client.force_authenticate(user=create_active_user)
        response = api_client.post(self.url, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
