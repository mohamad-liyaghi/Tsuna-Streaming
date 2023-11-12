import pytest
from django.urls import reverse
from rest_framework import status
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestCommentRetrieveView:
    @pytest.fixture(autouse=True)
    def setup(self, video, comment):
        self.url_name = "comments:comment_detail"
        self.video = video
        self.comment = comment
        self.content_type_id = get_content_type_model(model=type(self.video)).id

    def test_get_unauthorized(self, api_client):
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            )
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_authorized(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            )
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_not_found(self, api_client, user, create_unique_uuid):
        api_client.force_authenticate(user=user)
        response = api_client.get(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": create_unique_uuid,
                },
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
