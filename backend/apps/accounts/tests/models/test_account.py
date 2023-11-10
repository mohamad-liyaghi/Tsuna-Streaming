import pytest


@pytest.mark.django_db
def test_full_name_property(user):
    assert user.full_name == user.first_name + " " + user.last_name
