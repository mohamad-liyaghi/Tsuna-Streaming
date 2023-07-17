import pytest


@pytest.mark.django_db
def test_create_deactive_user(create_deactive_user):
    assert not create_deactive_user.is_active


@pytest.mark.django_db
def test_create_active_user(create_active_user):
    assert create_active_user.is_active


@pytest.mark.django_db
def test_create_superuser(create_superuser):
    assert create_superuser.is_superuser
    assert create_superuser.is_staff
    assert create_superuser.is_active
