import pytest
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from accounts.models import VerificationToken


@pytest.mark.django_db
class TestTokenModel:

    @pytest.fixture(autouse=True)
    def setup(self, create_deactive_user):
        self.user = create_deactive_user
        self.token = self.user.verification_tokens.first()

    def test_token_has_token(self):
        assert self.token.token is not None

    def test_check_token_is_valid(self):
        """By default the token is valid"""
        assert self.token.is_valid is True

    def test_token_is_not_valid(self):
        self.token.expire_at = timezone.now() - timedelta(minutes=11)
        self.token.save()
        assert self.token.is_valid is False
    
    def test_delete_token_after_user_deletion(self):
        """When a user is deleted, the token is deleted too"""
        self.user.delete()
        assert VerificationToken.objects.count() == 0

    def test_create_duplicate(self):
        assert self.user.verification_tokens.count() == 1
        with pytest.raises(PermissionDenied):
            VerificationToken.objects.create(user=self.user)

    def test_create_for_active_account(self, create_active_user):
        with pytest.raises(ValidationError):
            VerificationToken.objects.create(user=create_active_user)
