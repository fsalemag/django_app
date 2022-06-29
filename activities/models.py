from django.db import models
from users.models import MyUser
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class FavoriteCategory(models.Model):
    ...


class Tags(models.Model):
    ...


class Activity(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    time_of_event = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    participants = models.ManyToManyField(MyUser, related_name="participants")
    max_n_participants = models.IntegerField()

    waiting_list_enabled = models.BooleanField(default=False)
    waiting_list = models.ManyToManyField(MyUser, related_name="waiting_list", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('activities-detail', kwargs={'pk': self.pk, 'category': self.category.name})

    @property
    def is_full(self):
        return self.participants.count() >= self.max_n_participants

class FavouriteActivity(models.Model):
    ...
