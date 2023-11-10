import pytest
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from accounts.models import VerificationToken


@pytest.mark.django_db
class TestTokenModel:
    @pytest.fixture(autouse=True)
    def setup(self, inactive_user):
        self.user = inactive_user
        self.token = self.user.verification_tokens.first()

    def test_token_is_created_for_inactive_user(self):
        assert self.token.token is not None

    def test_create_for_active_account(self, user):
        with pytest.raises(ValidationError):
            VerificationToken.objects.create(user=user)

    def test_token_is_valid(self):
        assert self.token.is_valid is True

    def test_create_duplicate_fails(self):
        assert self.user.verification_tokens.count() == 1
        with pytest.raises(PermissionDenied):
            VerificationToken.objects.create(user=self.user)

    def test_token_is_expired(self):
        """Token is expired after 10 minutes"""
        self.token.expire_at = timezone.now() - timedelta(minutes=11)
        self.token.save()
        assert self.token.is_valid is False

    def test_delete_token_after_user_deletion(self):
        verification_id = self.token.id
        self.user.delete()
        assert not VerificationToken.objects.filter(id=verification_id).exists()
