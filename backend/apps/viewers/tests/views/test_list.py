import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import Account
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestViewerListView:
    @pytest.fixture(autouse=True)
    def setup(self, video):
        self.url_name = "viewers:list"
        self.video = video
        self.content_type_id = get_content_type_model(model=type(self.video)).id

    def test_get_unauthorized(self, api_client):
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            )
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_no_viewer(self, api_client, another_user):
        user = another_user
        api_client.force_authenticate(user=user)
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 0

    def test_list_viewer_in_cache(self, api_client, another_user, cached_viewer):
        api_client.force_authenticate(user=another_user)
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 1

    def test_list_viewer_db(self, api_client, another_user, viewer):
        api_client.force_authenticate(user=another_user)
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 1

    def test_get_not_found(self, api_client, another_user, create_unique_uuid):
        user = another_user
        api_client.force_authenticate(user=user)
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": create_unique_uuid,
                },
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_content_object_not_found(
        self, api_client, another_user, create_unique_uuid
    ):
        user = another_user
        api_client.force_authenticate(user=user)
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={"content_type_id": "1234", "object_token": self.video.token},
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
