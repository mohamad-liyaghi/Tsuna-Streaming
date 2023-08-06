import pytest
from django.urls import reverse
from rest_framework import status
from votes.models import Vote
from accounts.models import Account
from channels.models import Channel
from core.utils import get_content_type_model


@pytest.mark.django_db
class TestVoteDeleteView:
    @pytest.fixture(autouse=True)
    def setup(self, create_video):
        self.url_name = "votes:delete"
        self.video = create_video
        self.content_type_id = get_content_type_model(self.video.__class__, return_id=True)

    def test_delete_unauthorized(self, api_client):
        response = api_client.delete(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            }),
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_vote_in_db(self, api_client, create_vote):
        vote = create_vote
        api_client.force_authenticate(user=vote.user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            }),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Vote.objects.get_from_cache(
            channel=vote.channel,
            user=vote.user,
            content_object=vote.content_object
        )

    def test_delete_vote_in_cache(self, api_client, create_cached_vote):
        user = Account.objects.get(id=create_cached_vote['user'])
        channel = Channel.objects.get(id=create_cached_vote['channel'])

        api_client.force_authenticate(user=user)

        response = api_client.delete(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            }),
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Vote.objects.get_from_cache(
            channel=channel,
            user=user,
            content_object=create_cached_vote['content_object']
        )

    def test_delete_no_vote(self, create_active_user, api_client):
        user = create_active_user
        api_client.force_authenticate(user=user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": self.video.token
            }),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_not_found(self, api_client, create_active_user, create_unique_uuid):
        user = create_active_user
        api_client.force_authenticate(user=user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={
                "content_type_id": self.content_type_id,
                "object_token": create_unique_uuid
            })
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_content_object_not_found(
            self, api_client, create_active_user, create_unique_uuid
    ):
        user = create_active_user
        api_client.force_authenticate(user=user)
        response = api_client.delete(
            reverse(self.url_name, kwargs={
                "content_type_id": '1234',
                "object_token": self.video.token
            })
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
