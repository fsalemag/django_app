from datetime import datetime, timedelta

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from utils.test_utils import create_activities_and_categories, create_user_and_profile
from ..views import *


class ActivityTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        activities = {
            "football": {
                "count": 10,
                "date": datetime.now() - timedelta(days=5),
            },
            "tennis": {
                "count": 7,
                "date": datetime.now() - timedelta(days=4),
            },
            "padel": {
                "count": 3,
                "date": datetime.now() - timedelta(days=5),
            }
        }

        user, _ = create_user_and_profile("dummy@dummy.com")
        create_activities_and_categories(activities)


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        self.user = AnonymousUser()
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        pass

    def test_categories_page_status_code(self):
        request = self.factory.get("activities-categories")
        request.user = self.user

        response = CategoryView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_categories_page(self):
        url = reverse("activities-categories")

        response = self.client.get(url)
        context = response.context

        self.assertEqual(
            list(context["category_list"]),
            list((
                Category.objects.get(name="football"),
                Category.objects.get(name="tennis"),
                Category.objects.get(name="padel"),
            ))
        )
