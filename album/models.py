from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateField()

    def __str__(self):
        return self.title

