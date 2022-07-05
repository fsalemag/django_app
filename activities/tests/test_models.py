from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.utils import timezone

from users.models import MyUser
from utils.test_utils import create_activities_and_categories, create_user_and_profile
from ..models import Category, Activity, ActivityVote


class ActivityModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        activities = {
            "football": {
                "count": 10,
                "date": timezone.now() - timedelta(days=5),
                "max_participants": 1,
            },
            "tennis": {
                "count": 7,
                "date": timezone.now() + timedelta(days=4),
            },
            "padel": {
                "count": 3,
                "date": timezone.now() - timedelta(days=5),
            }
        }

        user, _ = create_user_and_profile("dummy@dummy.com")
        create_activities_and_categories(activities)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        self.anonymous_user = AnonymousUser()
        self.my_user = MyUser.objects.get(email="dummy@dummy.com")
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        pass

    def test_category_str(self):
        category = Category.objects.get(name="football")
        self.assertEqual(category.__str__(), "football")

    def test_activity_vote_str(self):
        activity_vote = ActivityVote.objects.create(voter=self.my_user, score=3)
        self.assertEqual(activity_vote.__str__(), "dummy@dummy.com: 3 (1)")

    def test_activity_str(self):
        activity = Activity.objects.all()[0]
        self.assertEqual(activity.__str__(), "Dummy Activity")

    def test_activity_is_past(self):
        activity = Activity.objects.filter(category__name="football")[0]
        self.assertTrue(activity.is_past)

        activity = Activity.objects.filter(category__name="tennis")[0]
        self.assertFalse(activity.is_past)

    def test_activity_is_full(self):
        activity = Activity.objects.filter(max_n_participants=1)[0]
        self.assertFalse(activity.is_full)

        activity.participants.add(self.my_user)
        self.assertTrue(activity.is_full)

    def test_activity_score(self):
        activity = Activity.objects.filter(category__name="padel")[0]
        self.assertIsNone(activity.score)

        for i in range(1, 5):
            vote = ActivityVote.objects.create(voter=self.my_user, score=i)
            activity.votes.add(vote)

        self.assertEqual(activity.score, 2.5)

    def test_activity_absolute_url(self):
        activity = Activity.objects.get(pk=1)
        self.assertEqual(
            activity.get_absolute_url(),
            '/activities/category/football/1'
        )
