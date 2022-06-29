from django.shortcuts import render
from django.views.generic import DetailView


def index(request):
    return render(request, "home/index.html")
