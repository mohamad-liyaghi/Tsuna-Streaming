import pytest  # noqa
import uuid
import time
from apps.core.tests.fixtures import *  # noqa
from apps.accounts.tests.fixtures import *  # noqa
from apps.memberships.tests.fixtures import *  # noqa
from apps.channels.tests.fixtures import *  # noqa
from apps.channel_subscribers.tests.fixtures import *  # noqa
from apps.channel_admins.tests.fixtures import *  # noqa
from apps.votes.tests.fixtures import *  # noqa
from apps.videos.tests.fixtures import *  # noqa
from apps.viewers.tests.fixtures import *  # noqa
from apps.comments.tests.fixtures import *  # noqa
from apps.musics.tests.fixtures import *  # noqa


@pytest.fixture
def create_unique_uuid():
    """Create a unique uuid based on time."""
    time_based_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))
    return time_based_uuid
