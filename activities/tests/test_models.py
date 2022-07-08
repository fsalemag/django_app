from ..models import Category, Activity, ActivityVote


class TestActivityModel:

    def test_category_str(self):
        category = Category.objects.get(name="football")
        assert category.__str__() == "football"

    def test_activity_vote_str(self, my_user):
        activity_vote = ActivityVote.objects.create(voter=my_user, score=3)
        assert activity_vote.__str__() == "dummy@dummy.com: 3 (1)"

    def test_activity_str(self):
        activity = Activity.objects.all()[0]
        assert activity.__str__() == "Dummy Activity"

    def test_activity_is_past(self):
        activity = Activity.objects.filter(category__name="football")[0]
        assert activity.is_past

        activity = Activity.objects.filter(category__name="tennis")[0]
        assert not activity.is_past

    def test_activity_is_full(self, my_user):
        activity = Activity.objects.filter(max_n_participants=1)[0]
        assert not activity.is_full

        activity.participants.add(my_user)
        assert activity.is_full

    def test_activity_score(self, my_user):
        activity = Activity.objects.filter(category__name="padel")[0]
        assert activity.score is None

        for i in range(1, 5):
            vote = ActivityVote.objects.create(voter=my_user, score=i)
            activity.votes.add(vote)

        assert activity.score == 2.5

    def test_activity_absolute_url(self):
        activity = Activity.objects.get(pk=1)
        assert activity.get_absolute_url() == '/activities/category/football/1'
