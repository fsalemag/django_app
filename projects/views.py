from django.shortcuts import render
from django.http import HttpResponse

from .models import Word

def test(request):
    words = Word.objects.order_by('-word')
    return render(request, "projects/index.html", context={"words": words})
