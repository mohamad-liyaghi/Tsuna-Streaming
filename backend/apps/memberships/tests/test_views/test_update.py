import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestMembershipUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, create_membership):
        self.url_name = "memberships:membership_detail"
        self.membership = create_membership
        self.data = {
            "title": "Updated Membership",
            "description": "Updated Description",
            "price": 100,
            "active_months": 12,
            "is_available": False,
        }

    def test_update_unauthorized(self, api_client):
        response = api_client.put(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_superuser(self, api_client, create_superuser):
        api_client.force_authenticate(create_superuser)
        response = api_client.put(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == self.data["title"]
        assert response.data["description"] == self.data["description"]
        assert response.data["price"] == self.data["price"]
        assert response.data["active_months"] == self.data["active_months"]
        assert response.data["is_available"] == self.data["is_available"]

    def test_update_by_premium_user(self, api_client, create_premium_user):
        api_client.force_authenticate(create_premium_user)
        response = api_client.put(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_by_normal_user(self, api_client, create_active_user):
        api_client.force_authenticate(create_active_user)
        response = api_client.put(
            reverse(
                self.url_name,
                kwargs={"membership_token": self.membership.token}
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_not_found(
            self, create_superuser, api_client, create_unique_uuid
    ):
        api_client.force_authenticate(create_superuser)
        response = api_client.put(
            reverse(
                self.url_name,
                kwargs={"membership_token": create_unique_uuid}
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
