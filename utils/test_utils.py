from activities.models import Category, Activity
from users.models import MyUser


def create_activities_and_categories(config):
    user = MyUser.objects.create(
        email="dummy@dummy.com",
        password="dummy_password",
    )

    for category, values in config.items():
        category = Category.objects.create(name=category, description=f"Description {category}")

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
