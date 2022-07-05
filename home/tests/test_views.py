from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from activities.models import Category
from utils.test_utils import create_activities_and_categories, create_user_and_profile
from ..views import index


class HomeTest(TestCase):
    index_url = reverse("home-index")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        activities = {
            "football": {
                "count": 3,
                "date": timezone.now() - timedelta(days=5),
            },
            "tennis": {
                "count": 1,
                "date": timezone.now() - timedelta(days=4),
            },
            "padel": {
                "count": 2,
                "date": timezone.now() - timedelta(days=5),
            },
            "volleyball": {
                "count": 4,
                "date": timezone.now() - timedelta(days=15),
            },
            "basketball": {
                "count": 5,
                "date": timezone.now() - timedelta(days=15),
            },
            "handball": {
                "count": 7,
                "date": timezone.now() - timedelta(days=15)
            },
            "rugby": {
                "count": 12,
                "date": timezone.now() - timedelta(days=32)
            }
        }

        user, _ = create_user_and_profile(email="dummy@dummy.com")
        create_activities_and_categories(activities, email=user.email)


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
