from django.core.files import File
import mock
import pytest


@pytest.fixture
def create_file():
    """
    Create a mock file
    """
    file_mock = mock.MagicMock(spec=File)
    file_mock.name = 'sample.mp4'
    file_mock.size = 1
    return file_mock
