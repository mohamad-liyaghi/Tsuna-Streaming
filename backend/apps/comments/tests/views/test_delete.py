import pytest
from django.urls import reverse
from rest_framework import status
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestCommentDeleteView:
    @pytest.fixture(autouse=True)
    def setup(self, video, comment):
        self.url_name = "comments:comment_detail"
        self.video = video
        self.comment = comment
        self.content_type_id = get_content_type_model(model=type(self.video)).id

    def test_delete_unauthorized(self, api_client):
        response = api_client.put(
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

    def test_delete_by_comment_owner(self, api_client):
        api_client.force_authenticate(user=self.comment.user)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            )
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_others(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_by_channel_admin(self, api_client, channel_admin):
        api_client.force_authenticate(user=channel_admin.user)
        response = api_client.delete(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            )
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_not_found(self, api_client, user, create_unique_uuid):
        api_client.force_authenticate(user=user)
        response = api_client.delete(
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
