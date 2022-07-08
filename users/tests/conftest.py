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
                "count": 1,
                "date": timezone.now() - timedelta(days=5),
            },
            "tennis": {
                "count": 1,
                "date": timezone.now() - timedelta(days=4),
            },
            "padel": {
                "count": 1,
                "date": timezone.now() - timedelta(days=5),
            }
        }

        user, _ = create_user_and_profile(email=email)
        create_activities_and_categories(activities, email=user.email)
