import pytest
from django.urls import reverse
from rest_framework import status
from core.utils import get_content_type_model
from comments.models import Comment


@pytest.mark.django_db
class TestCommentCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, video):
        self.url_name = "comments:comment_list_create"
        self.video = video
        self.content_type_id = get_content_type_model(model=type(self.video)).id
        self.data = {"body": "test comment"}

    def test_create_unauthorized(self, api_client):
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_reply(self, api_client, user, comment):
        self.data["parent"] = comment.token
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            ),
            data=self.data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_comment_not_allowed(self, api_client, user):
        api_client.force_authenticate(user=user)
        self.video.allow_comment = False
        self.video.save()
        self.video.refresh_from_db()

        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": self.video.token,
                },
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not self.video.allow_comment

    def test_create_object_not_found(self, api_client, user, create_unique_uuid):
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse(
                self.url_name,
                kwargs={
                    "content_type_id": self.content_type_id,
                    "object_token": create_unique_uuid,
                },
            ),
            data=self.data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
