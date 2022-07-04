from django.contrib.auth.models import AnonymousUser
from users.models import MyUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from datetime import datetime, timedelta

from ..views import index
from activities.models import Activity, Category

class HomeTest(TestCase):
    index_url = reverse("home-index")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user = MyUser.objects.create(
            email="dummy@dummy.com",
            password="dummy_password",
        )

        activities = {
            "football": {
                "count": 3,
                "date": datetime.now() - timedelta(days=5),
            },
            "tennis": {
                "count": 1,
                "date": datetime.now() - timedelta(days=4),
            },
            "padel": {
                "count": 2,
                "date": datetime.now() - timedelta(days=5),
            },
            "volleyball": {
                "count": 4,
                "date": datetime.now() - timedelta(days=15),
            },
            "basketball": {
                "count": 5,
                "date": datetime.now() - timedelta(days=15),
            },
            "handball": {
                "count": 7,
                "date": datetime.now() - timedelta(days=15)
            },
            "rugby": {
                "count": 12,
                "date": datetime.now() - timedelta(days=32)
            }
        }

        for category, values in activities.items():
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


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        """ No functionality of home page requires a logged-in user"""
        self.user = AnonymousUser()
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        pass

    def test_index_status_code(self):
        request = self.factory.get(self.index_url)
        request.user = self.user

        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_index_context(self):
        request = self.factory.get(self.index_url)
        request.user = self.user

        response = self.client.get(self.index_url)
        context = response.context[-1]

        expected_context = {
            'n_activities': 34,
            'n_users': 1,
            'n_month_activities': 22,
        }

        for variable in expected_context.keys():
            self.assertEqual(context[variable], expected_context[variable])

        self.assertEqual(
            list(context["top_categories"]),
            list((
                Category.objects.get(name="rugby"),
                Category.objects.get(name="handball"),
                Category.objects.get(name="basketball"),
            ))
        )

        self.assertEqual(
            list(context["trending_categories"]),
            list((
                Category.objects.get(name="football"),
                Category.objects.get(name="padel"),
                Category.objects.get(name="tennis"),
            ))
        )
