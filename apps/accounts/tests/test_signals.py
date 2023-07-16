import pytest


@pytest.mark.django_db
def test_create_token_deactive_user(create_deactive_user):
    """Test create token for deactive user."""
    assert not create_deactive_user.is_active
    assert create_deactive_user.tokens.count() == 1


@pytest.mark.django_db
def test_not_create_token_for_superuser(create_superuser):
    """Test not create token for superuser."""
    assert create_superuser.is_active
    assert create_superuser.tokens.count() == 0
