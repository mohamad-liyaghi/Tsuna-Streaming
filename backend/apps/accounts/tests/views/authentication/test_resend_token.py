import pytest
from datetime import timedelta
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTokenResendView:
    def setup(self):
        self.url_path = reverse("accounts:resend_verification")

    def test_resend_verification_code(self, inactive_user, api_client):
        verification = inactive_user.verification_tokens.first()
        verification.expire_at -= timedelta(days=2)
        verification.save()

        assert not verification.is_valid

        response = api_client.post(
            self.url_path, {"user": inactive_user.token}, format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert inactive_user.verification_tokens.count() == 2

    def test_resend_valid_code_exist_fails(self, inactive_user, api_client):
        """
        Not send verification token if an active one already exists
        """
        verification = inactive_user.verification_tokens.first()
        assert verification.is_valid

        response = api_client.post(
            self.url_path, {"user": inactive_user.token}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert inactive_user.verification_tokens.count() == 1

    def test_resend_for_active_user_fails(self, user, api_client):
        assert user.is_active

        response = api_client.post(self.url_path, {"user": user.token}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resend_invalid_data_fails(self, api_client):
        response = api_client.post(self.url_path)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resend_authenticated_fails(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.post(self.url_path, {}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
