from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    intro_image = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateField()
    content = models.TextField()

    def __str__(self):
        return self.title
