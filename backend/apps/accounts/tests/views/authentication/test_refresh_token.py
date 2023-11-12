import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestObtainTokenView:
    @pytest.fixture(autouse=True)
    def setup(self, user):
        """
        Set password for the user and create data for the test.
        """
        password = "FAKEpass1234"
        user.set_password(password)
        user.save()

        self.data = {"email": user.email, "password": password}
        self.url_path = reverse("accounts:login")

    def test_get_access_token(self, api_client):
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_get_access_token_non_existing_user(self, api_client):
        response = api_client.post(
            self.url_path,
            {"email": "non@exist.com", "password": "1234EErr"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {
            "detail": "No active account found with the given credentials"
        }

    def test_get_access_token_invalid_data(self, api_client):
        self.data["password"] = "invalid_password"
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_access_token_inactive_user(self, inactive_user, api_client):
        self.data["email"] = inactive_user.email
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_authenticated(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
