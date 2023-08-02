import pytest
from django.urls import reverse
from rest_framework import status
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestCommentUpdateView:
    @pytest.fixture(autouse=True)
    def setup(self, create_video, create_comment):
        self.url_name = "comments:comment_detail"
        self.video = create_video
        self.comment = create_comment
        self.content_type_id = get_content_type_model(
            self.video.__class__, return_id=True
        )
        self.data = {
            "body": "updated comment"
        }

    def test_update_unauthorized(self, api_client):
        response = api_client.put(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token,
                "comment_token": self.comment.token
            }),
            data=self.data,
            format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_comment_owner(self, api_client):
        api_client.force_authenticate(user=self.comment.user)
        response = api_client.put(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token,
                "comment_token": self.comment.token
            }),
            data=self.data,
            format="json"
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_others(self, create_superuser, api_client):
        api_client.force_authenticate(user=create_superuser)
        response = api_client.put(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token,
                "comment_token": self.comment.token
            }),
            data=self.data,
            format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert create_superuser != self.comment.user

    def test_update_not_found(self, api_client, create_unique_uuid):
        api_client.force_authenticate(user=self.comment.user)
        response = api_client.put(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token,
                "comment_token": create_unique_uuid
            }),
            data=self.data,
            format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
