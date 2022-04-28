import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Post


class PostModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        # title = models.CharField(max_length=100)
        # intro_image = models.CharField(max_length=200)
        # description = models.TextField()
        # date_posted = models.DateField()
        # content = models.TextField()
        future_question = Post(title="test", date_posted=time)
        self.assertIs(future_question.date_posted > timezone.now(), False)
