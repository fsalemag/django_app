import pytest
from django.contrib.auth.models import AnonymousUser

from utils.test_utils import create_user_and_profile


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """ Enable every test to access the database """
    pass


@pytest.fixture()
def my_user():
    """ Used mostly to represent the creator af an activity"""
    user, _ = create_user_and_profile(email="dummy@dummy.com")
    return user


@pytest.fixture
def other_user():
    """ Used mostly as non-creator of activity"""
    user, _ = create_user_and_profile(email="dummy2@dummy.com")
    return user


@pytest.fixture
def anonymous_user():
    """ Not logged in user """
    return AnonymousUser()


@pytest.fixture(params=("my_user", "other_user", "anonymous_user"))
def users(request):
    """ If provided runs same test for creator, authenticated user and anonymous user"""
    return request.getfixturevalue(request.param)
