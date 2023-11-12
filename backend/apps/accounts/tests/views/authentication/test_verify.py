import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import Account, VerificationToken


@pytest.mark.django_db
class TestVerifyUserView:
    @pytest.fixture(autouse=True)
    def setup(self, inactive_user):
        self.user = inactive_user
        self.verification_code = self.user.verification_tokens.first().token
        self.user_token = self.user.token

        self.url_name = "accounts:verify"
        self.url_path = reverse(
            self.url_name,
            kwargs={
                "user_token": self.user_token,
                "verification_token": self.verification_code,
            },
        )

    def test_verify_user_false_code_fails(self, api_client, create_unique_uuid):
        url_path = reverse(
            self.url_name,
            kwargs={
                "user_token": self.user.token,
                "verification_token": create_unique_uuid,
            },
        )
        response = api_client.get(url_path)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_verify_user(self, api_client):
        response = api_client.get(self.url_path)
        self.user.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert self.user.is_active

    def test_verify_active_user_fails(self, api_client, user):
        url_path = reverse(
            self.url_name,
            kwargs={
                "user_token": user.token,
                "verification_token": VerificationToken.objects.first().token,
            },
        )
        response = api_client.get(url_path)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verify_invalid_user_fails(self, api_client, create_unique_uuid):
        self.url_path = reverse(
            self.url_name,
            kwargs={
                "user_token": create_unique_uuid,
                "verification_token": self.verification_code,
            },
        )
        response = api_client.get(self.url_path)
        assert not Account.objects.filter(token=create_unique_uuid).exists()
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_verify_authenticated_fails(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN
