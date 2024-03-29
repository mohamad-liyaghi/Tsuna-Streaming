import pytest
from django.urls import reverse
from rest_framework import status
from votes.models import Vote
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestVoteCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, video):
        self.url_name = "votes:create"
        self.video = video
        self.content_type_id = get_content_type_model(model=type(self.video)).id

    def test_create_unauthorized(self, api_client):
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            ),
            {},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_duplicated(self, vote, api_client):
        vote = vote
        api_client.force_authenticate(user=vote.user)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": vote.content_object.token,
                },
            ),
            {},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_authorized(self, api_client, another_user):
        user = another_user
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            ),
            {},
        )
        vote_status = Vote.objects.get_from_cache(
            channel=self.video.channel, user=user, content_object=self.video
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert vote_status

    def test_create_not_found(self, api_client, another_user, create_unique_uuid):
        user = another_user
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": create_unique_uuid,
                },
            ),
            {},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_content_object_not_found(
        self, api_client, another_user, create_unique_uuid
    ):
        user = another_user
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={"content_type_id": "1234", "object_token": self.video.token},
            ),
            {},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
