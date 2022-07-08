from datetime import timedelta
from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from activities.models import Category, Activity
from users.models import MyUser, UserProfile


def create_activities_and_categories(config: dict, email: str = "dummy@dummy.com") -> None:
    """ Creates activities based on config supplied.
    config must be in the form
        {
            "<category>": {
                "count": <number of activities>,
                "date": <time_of_event / date_created>,
            },
            ...
        }
    Configuration can be extended to the other fields, but I haven't had the need so far.
    """
    user = MyUser.objects.get(
        email=email
    )

    for category, values in config.items():
        category, _ = Category.objects.get_or_create(name=category, description=f"Description {category}")

        for i in range(values["count"]):
            activity = Activity.objects.create(
                category=category,
                creator=user,
                title="Dummy Activity",
                description="Dummy Description",
                location="Dummy Location",
                time_of_event=values["date"],
                max_n_participants=values.get("max_participants", 5),
            )

            activity.created_on = values["date"]
            activity.save()


def create_user_and_profile(email: str) -> Tuple[MyUser, UserProfile]:
    """ Create or get both user and correspondent profile

    Cannot use get or create user because I overwrite the password to be `dummy_password` on its encrypted form.
    There might be a more elegant way of doing this
    """
    try:
        user = MyUser.objects.get(email=email)
    except ObjectDoesNotExist:
        user = MyUser.objects.create(email=email, password="qwerty123")
        user.set_password("dummy_password")
        user.save()

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        date_of_birth=timezone.now() - timedelta(days=365*25),
        gender="f",
        phone_number=123123123,
    )

    return user, profile
