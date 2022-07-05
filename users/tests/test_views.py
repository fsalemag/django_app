from datetime import datetime, timedelta

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from utils.test_utils import create_activities_and_categories, create_user_and_profile
from ..models import MyUser, UserProfile
from ..views import ProfileActivityView, ProfileView


class UserTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        activities = {
            "football": {
                "count": 1,
                "date": datetime.now() - timedelta(days=5),
            },
            "tennis": {
                "count": 1,
                "date": datetime.now() - timedelta(days=4),
            },
            "padel": {
                "count": 1,
                "date": datetime.now() - timedelta(days=5),
            }
        }

        user, _ = create_user_and_profile(email="dummy@dummy.com")
        create_activities_and_categories(activities, email=user.email)

        user, _ = create_user_and_profile(email="dummy2@dummy.com")
        create_activities_and_categories(activities, email=user.email)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        self.my_user = MyUser.objects.get(email="dummy@dummy.com")
        self.other_user = MyUser.objects.get(email="dummy2@dummy.com")
        self.anonymous_user = AnonymousUser()
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        pass

    def test_profile_page_logged_in_user_status_code(self):
        request = self.factory.get("users-profile")
        request.user = self.my_user

        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_page_logged_in_user(self):
        self.assertTrue(self.client.login(
            email="dummy@dummy.com", password="dummy_password"
        ))
        url = reverse("users-profile")
        response = self.client.get(url)
        context = response.context[-1].dicts[-1]

        self.assertEqual(UserProfile.objects.get(user__email="dummy@dummy.com"), context["user_profile"])

    def test_profile_page_not_logged_in_user(self):
        url = reverse("users-profile")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('account_login'), response.url)

    def test_profile_page_other_user(self):
        url = reverse("users-external-profile", kwargs={"pk": 2})
        response = self.client.get(url)
        context = response.context[-1].dicts[-1]

        self.assertEqual(UserProfile.objects.get(user__email="dummy2@dummy.com"), context["user_profile"])


    def test_activities_mine_page_status_code(self):
        request = self.factory.get("users-activities")
        request.user = self.my_user

        response = ProfileActivityView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_activities_mine_page(self):
        self.assertTrue(self.client.login(
            email="dummy@dummy.com", password="dummy_password"
        ))

        url = reverse("users-activities")

        response = self.client.get(url)
        context = response.context_data

        self.assertEqual(UserProfile.objects.get(user__email="dummy@dummy.com"), context["userprofile"])
