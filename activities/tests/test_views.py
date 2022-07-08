from datetime import timedelta

from django.shortcuts import reverse
from django.utils import timezone

from users.models import MyUser, UserProfile
from ..models import Activity, Category, ActivityVote
from ..views import CategoryView, ActivityCreateView, ActivityEditDetailView


class TestActivityView:
    categories_url = "activities-categories"
    activities_url = "activities-index"
    activities_in_category_url = "activities-category"
    activity_detail_url = "activities-detail"
    activity_create = "activities-create"
    activity_edit = "activities-edit-detail"

    def test_categories_page_status_code(self, rf, my_user):
        request = rf.get(self.categories_url)
        request.user = my_user

        response = CategoryView.as_view()(request)
        assert response.status_code == 200

    def test_categories_page(self, client):
        context = client.get(reverse(self.categories_url)).context

        assert list(context["category_list"]) == \
            list((
                Category.objects.get(name="football"),
                Category.objects.get(name="tennis"),
                Category.objects.get(name="padel"),
            ))

    def test_activity_list(self, client):
        context = client.get(reverse(self.activities_url)).context

        assert list(context.get("object_list")) == list(Activity.objects.all())

        url = reverse(self.activities_in_category_url, kwargs={"category": "football"})
        context = client.get(url).context

        assert list(context.get("object_list")) == list(Activity.objects.filter(category__name="football"))

    # TODO parametrize every query parameter
    def test_activity_filters(self, client):
        url = reverse(self.activities_url) + "?max_participants=1"

        context = client.get(url).context

        assert list(context.get("object_list")) == \
               list(Activity.objects.filter(max_n_participants__lte=1))

    def test_activity_detail_view(self, my_user, client):
        url = reverse(self.activity_detail_url, kwargs={'category': "football", 'pk': 1})

        activity = Activity.objects.get(pk=1)
        vote = ActivityVote.objects.create(voter=my_user, score=3)
        activity.votes.add(vote)
        activity.participants.add(my_user)

        context = client.get(url).context

        assert len(context.get("voters")) == 1
        assert len(context.get("profiles")) == 1

        assert MyUser.objects.get(pk=context.get("voters")[0]).email == "dummy@dummy.com"

        assert list(context.get("profiles")) == list(UserProfile.objects.filter(user__email="dummy@dummy.com"))

    def test_activity_create_view(self, my_user, rf):
        data = {
            'title': 'test_title',
            'description': 'test_description',
            'location': 'test_location',
            'time_of_event': timezone.now() + timedelta(days=1),
            'max_n_participants': 10,
            'category': Category.objects.all()[0].pk
        }

        request = rf.post(reverse(self.activity_create), data)
        request.user = my_user

        response = ActivityCreateView.as_view()(request)

        # returns redirect to my activities
        assert response.status_code == 302
        assert Activity.objects.filter(title='test_title').count() == 1

    def test_activity_edit_view_get(self, my_user, rf):
        url = reverse(self.activity_edit, kwargs={"category": "football", "pk": 1})

        request = rf.get(url)
        request.user = my_user
        response = ActivityEditDetailView.as_view()(request, pk=1)

        assert response.status_code == 200

    # def test_activity_edit_view_post(self, rf):
    #     url = reverse('activities-edit-detail', kwargs={"category": "football", "pk": 1})
    #
    #     request = rf.post(url, {"action": "unjoin"})
    #     request.user = self.my_user
    #     response = ActivityEditDetailView.as_view()(request, pk=1)
    #     assert response.status_code == 200
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
    #     request = rf.post(url, data)
    #     request.user = self.my_user
    #
    #     response = ActivityCreateView.as_view()(request)
    #
    #     # returns redirect to my activities
    #     assert response.status_code == 302
    #     assert Activity.objects.filter(title='test_title').count() == 1
