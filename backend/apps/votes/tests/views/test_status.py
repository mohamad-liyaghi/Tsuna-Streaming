import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import Account
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestVoteStatusView:
    @pytest.fixture(autouse=True)
    def setup(self, video):
        self.url_name = "votes:status"
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

    def test_get_no_vote(self, api_client, another_user):
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
        assert response.data is None

    def test_get_with_vote_in_db(self, vote, api_client):
        user = vote.user
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

    def test_get_with_vote_in_cache(self, cached_vote, superuser, api_client):
        user = superuser
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
        assert response.data

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

    def test_delete_content_object_not_found(
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
