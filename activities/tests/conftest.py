from datetime import timedelta

import pytest
from django.utils import timezone

from utils.test_utils import create_activities_and_categories, create_user_and_profile


@pytest.fixture(
    autouse=True,
)
def activities():
    """ Populates database with some default values, for 2 users, it also creates the users"""
    for email in ("dummy@dummy.com", "dummy2@dummy.com"):
        activities = {
            "football": {
                "count": 10,
                "date": timezone.now() - timedelta(days=5),
                "max_participants": 1,
            },
            "tennis": {
                "count": 7,
                "date": timezone.now() - timedelta(days=4),
                "max_participants": 2,
            },
            "padel": {
                "count": 3,
                "date": timezone.now() - timedelta(days=5),
                "max_participants": 3,
            }
        }

        user, _ = create_user_and_profile(email=email)
        create_activities_and_categories(activities, email=user.email)
