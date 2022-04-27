from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Video

def album(request):
    return render(request, "album/index.html")


class Album(ListView):
    model = Video
    template_name = "album/index.html"
    ordering = ['-date_posted']
