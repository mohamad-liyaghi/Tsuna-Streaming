import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Fixture for creating an API client"""
    return APIClient()
