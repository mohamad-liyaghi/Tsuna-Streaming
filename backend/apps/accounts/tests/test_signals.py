import pytest


@pytest.mark.django_db
def test_token_is_created_for_inactive_user(inactive_user):
    """Test create token for inactive user."""
    assert not inactive_user.is_active
    assert inactive_user.verification_tokens.count() == 1


@pytest.mark.django_db
def test_token_is_not_created_for_superuser(superuser):
    """Test not create token for superuser."""
    assert superuser.is_active
    assert superuser.verification_tokens.count() == 0
