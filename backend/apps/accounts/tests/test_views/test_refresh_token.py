import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestObtainTokenView:
    @pytest.fixture(autouse=True)
    def setup(self, create_active_user):
        """
        Set password for the user and create data for the test.
        """
        password = "FAKEpass1234"
        create_active_user.set_password(password)
        create_active_user.save()

        self.data = {"email": create_active_user.email, "password": password}
        self.url_path = reverse("accounts:login")

    def test_get_access_token(self, api_client):
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_get_access_token_non_existance_user(self, api_client):
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

    def test_get_access_token_inactive_user(self, create_deactive_user, api_client):
        self.data["email"] = create_deactive_user.email
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_authenticated(self, api_client, create_superuser):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.post(self.url_path, self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
