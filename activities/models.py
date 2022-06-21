from django.db import models
from users.models import MyUser


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
    time_of_event = models.DateField()
    created_on = models.DateField()
    updated_on = models.DateField()

    min_n_participants = models.IntegerField()
    max_n_participants = models.IntegerField()

    def __str__(self):
        return self.title


class FavouriteActivity(models.Model):
    ...
