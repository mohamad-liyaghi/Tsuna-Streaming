import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMembershipListView:
    def setup(self):
        self.url = reverse("memberships:membership")

    def test_get_unauthorized_fails(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_by_superuser(self, superuser, api_client):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_premium_user(self, premium_user, api_client):
        api_client.force_authenticate(user=premium_user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_normal_user(self, user, api_client):
        api_client.force_authenticate(user=user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
