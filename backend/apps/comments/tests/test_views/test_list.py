import pytest
from django.urls import reverse
from rest_framework import status
from core.utils import get_content_type_model
from comments.models import Comment


@pytest.mark.django_db
class TestCommentListView:
    @pytest.fixture(autouse=True)
    def setup(self, create_video):
        self.url_name = "comments:comment_list_create"
        self.video = create_video
        self.content_type_id = get_content_type_model(model=type(self.video)).id

    def test_get_unauthorized(self, api_client):
        response = api_client.get(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            })
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_no_comment(self, api_client, create_active_user):
        api_client.force_authenticate(user=create_active_user)
        response = api_client.get(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            })
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['count'] == 0

    def test_get_with_comment(
            self,
            api_client,
            create_comment,
            create_active_user
    ):
        api_client.force_authenticate(user=create_active_user)
        response = api_client.get(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            })
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['count'] == 1

    def test_show_only_parent_comments(
            self,
            create_comment,
            api_client,
            create_active_user
    ):
        # Create a child comment
        Comment.objects.create(
            user=create_active_user,
            content_object=self.video,
            body="child comment",
            parent=create_comment
        )

        api_client.force_authenticate(user=create_active_user)
        response = api_client.get(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            })
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['count'] == 1

    def test_get_not_found(
            self,
            api_client,
            create_active_user,
            create_unique_uuid
    ):
        api_client.force_authenticate(user=create_active_user)
        response = api_client.get(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": create_unique_uuid
            })
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
