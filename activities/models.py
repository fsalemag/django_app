from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils import timezone

from users.models import MyUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ActivityVote(models.Model):
    voter = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="votes")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True
    )
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.voter.email}: {self.score} ({self.pk})"


class Activity(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_activity")
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="activities_created")

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    time_of_event = models.DateTimeField()
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    participants = models.ManyToManyField(MyUser, related_name="activities")
    max_n_participants = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    waiting_list_enabled = models.BooleanField(default=False)
    waiting_list = models.ManyToManyField(MyUser, related_name="waiting_list", blank=True)

    votes = models.ManyToManyField(ActivityVote, related_name="activities_voted", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activities-detail', kwargs={'pk': self.pk, 'category': self.category.name})

    @property
    def is_full(self):
        return self.participants.count() >= self.max_n_participants

    @property
    def is_past(self):
        return self.time_of_event < timezone.now()

    @property
    def score(self):
        score = self.votes.aggregate(sum_score=Sum("score"), count_score=Count("score"))
        return round(score.get("sum_score") / score.get("count_score"), 1) if score.get("count_score", 0) != 0 else None

    def save(self, **kwargs):
        self.updated_on = timezone.now()
        super().save()
