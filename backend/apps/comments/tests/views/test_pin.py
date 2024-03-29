import pytest
from django.urls import reverse
from rest_framework import status
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestCommentPinView:
    @pytest.fixture(autouse=True)
    def setup(self, video, comment):
        self.url_name = "comments:comment_detail"
        self.video = video
        self.comment = comment
        self.content_type_id = get_content_type_model(model=type(self.video)).id
        self.data = {"pinned": True}

    def test_pin_unauthorized(self, api_client):
        response = api_client.patch(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            ),
            data=self.data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_pin_by_non_admin(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.patch(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            ),
            data=self.data,
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_pin_by_channel_admin(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.patch(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": self.comment.token,
                },
            ),
            data=self.data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert user.channel_admins.filter(channel=self.video.channel).exists()

    def test_pin_not_found(self, api_client, create_unique_uuid, user):
        api_client.force_authenticate(user=user)
        response = api_client.patch(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                    "comment_token": create_unique_uuid,
                },
            ),
            data=self.data,
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
