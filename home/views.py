from django.http import HttpResponse
from django.shortcuts import render

from .models import Post

def index(request):
    posts = Post.objects.order_by('-date_posted')
    return render(request, "home/index.html", context={"posts": posts})
