import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import Account


@pytest.mark.django_db
class TestRegisterUserView:

    def setup(self):
        """Default data for all tests"""
        self.data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
        }
        self.url_path = reverse('accounts:register')

    def test_register(self, api_client):
        response = api_client.post(
            self.url_path, self.data, format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Account.objects.count() == 1

    def test_register_duplicate_user(
            self, api_client, create_active_user
    ):
        """
        Test register with an active accounts email
        """
        self.data['email'] = create_active_user.email
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Account.objects.count() == 1
        assert Account.objects.first() == create_active_user

    def test_duplicate_deactive_user_email(
            self, api_client, create_deactive_user
    ):
        """
        Test register with an deactive accounts email
        """
        self.data['email'] = create_deactive_user.email
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_authenticated(
            self, api_client, create_superuser
    ):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
