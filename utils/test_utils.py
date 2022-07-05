from datetime import datetime, timedelta

from activities.models import Category, Activity
from users.models import MyUser, UserProfile


def create_activities_and_categories(config, email="dummy@dummy.com"):
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
                max_n_participants=5,
            )

            activity.created_on = values["date"]
            activity.save()


def create_user_and_profile(email):
    user, _ = MyUser.objects.get_or_create(
        email=email,
        password="dummy_password",
    )
    user.set_password("dummy_password")
    user.save()

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        date_of_birth=datetime.now() - timedelta(days=365*25),
        gender="f",
        phone_number=123123123,
    )

    return user, profile
