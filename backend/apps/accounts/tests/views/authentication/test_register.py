import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import Account


@pytest.mark.django_db
class TestRegisterUserView:
    def setup(self):
        self.data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "FakePasswordForNow",
        }
        self.url_path = reverse("accounts:register")

    def test_register(self, api_client):
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Account.objects.filter(email=self.data["email"]).exists()

    def test_register_duplicated_email_fails(self, api_client, user):
        self.data["email"] = user.email
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_authenticated_fail(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_duplicate_inactive_user_email(self, api_client, inactive_user):
        """
        Test register with an inactive accounts email
        """
        self.data["email"] = inactive_user.email
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
