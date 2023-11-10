import pytest


@pytest.mark.django_db
def test_inactive_user_is_not_active(inactive_user):
    assert not inactive_user.is_active


@pytest.mark.django_db
def test_active_user_is_active(user):
    assert user.is_active


@pytest.mark.django_db
def test_superuser_is_superuser(superuser):
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.is_active
