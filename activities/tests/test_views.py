from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from django.test import RequestFactory, TestCase
from django.utils import timezone

from users.models import MyUser, UserProfile
from utils.test_utils import create_activities_and_categories, create_user_and_profile
from ..models import Activity, Category, ActivityVote
from ..views import CategoryView, ActivityCreateView, ActivityEditDetailView


class ActivityViewTest(TestCase):

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
                "date": timezone.now() - timedelta(days=4),
                "max_participants": 2,
            },
            "padel": {
                "count": 3,
                "date": timezone.now() - timedelta(days=5),
                "max_participants": 3,
            }
        }

        user, _ = create_user_and_profile("dummy@dummy.com")
        create_activities_and_categories(activities)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        self.my_user = MyUser.objects.get(email="dummy@dummy.com")
        self.other_user, _ = create_user_and_profile(email="dummy2@dummy.com")
        self.anonymous_user = AnonymousUser()
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        pass

    def test_categories_page_status_code(self):
        request = self.factory.get("activities-categories")
        request.user = self.my_user

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

    def test_activity_list(self):
        url = reverse("activities-index")

        response = self.client.get(url)
        context = response.context

        self.assertEqual(
            list(context.get("object_list")),
            list(Activity.objects.all())
        )

        url = reverse("activities-category", kwargs={"category": "football"})
        response = self.client.get(url)
        context = response.context
        self.assertEqual(
            list(context.get("object_list")),
            list(Activity.objects.filter(category__name="football"))
        )

    def test_activity_filters(self):
        url = reverse("activities-index") + "?max_participants=1"

        response = self.client.get(url)
        context = response.context

        self.assertEqual(
            list(context.get("object_list")),
            list(Activity.objects.all()[:10])
        )

    def test_activity_detail_view(self):
        url = reverse('activities-detail', kwargs={'category': "football", 'pk': 1})

        activity = Activity.objects.get(pk=1)
        vote = ActivityVote.objects.create(voter=self.my_user, score=3)
        activity.votes.add(vote)
        activity.participants.add(self.my_user)

        response = self.client.get(url)
        context = response.context

        self.assertEqual(len(context.get("voters")), 1)
        self.assertEqual(len(context.get("profiles")), 1)

        self.assertEqual(
            MyUser.objects.get(pk=context.get("voters")[0]).email,
            "dummy@dummy.com"
        )

        self.assertEqual(
            list(context.get("profiles")),
            list(UserProfile.objects.filter(user__email="dummy@dummy.com"))
        )

    def test_activity_create_view(self):
        url = reverse('activities-create')
        data = {
            'title': 'test_title',
            'description': 'test_description',
            'location': 'test_location',
            'time_of_event': timezone.now() + timedelta(days=1),
            'max_n_participants': 10,
            'category': Category.objects.all()[0].pk
        }

        request = self.factory.post(url, data)
        request.user = self.my_user

        response = ActivityCreateView.as_view()(request)

        # returns redirect to my activities
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Activity.objects.filter(title='test_title').count(), 1)

    def test_activity_edit_view_get(self):
        url = reverse('activities-edit-detail', kwargs={"category": "football", "pk": 1})

        # Creator of activity
        request = self.factory.get(url)
        request.user = self.my_user
        response = ActivityEditDetailView.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 200)

        # Not logged in user
        request = self.factory.get(url)
        request.user = self.anonymous_user
        response = ActivityEditDetailView.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse("account_login"))

        # Other user
        request = self.factory.get(url)
        request.user = self.other_user
        response = ActivityEditDetailView.as_view()(request, pk=1)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse("home-index"))

    # def test_activity_edit_view_post(self):
    #     url = reverse('activities-edit-detail', kwargs={"category": "football", "pk": 1})
    #
    #     # join
    #     # unjoin
    #     # vote
    #     # join waiting list
    #     # unjoin waiting list
    #     # update activity
    #
    #     data = {
    #         'title': 'test_title',
    #         'description': 'test_description',
    #         'location': 'test_location',
    #         'time_of_event': timezone.now() + timedelta(days=1),
    #         'max_n_participants': 10,
    #         'category': Category.objects.all()[0].pk
    #     }
    #
    #     request = self.factory.post(url, data)
    #     request.user = self.my_user
    #
    #     response = ActivityCreateView.as_view()(request)
    #
    #     # returns redirect to my activities
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(Activity.objects.filter(title='test_title').count(), 1)
