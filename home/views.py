from django.shortcuts import render
from django.views.generic import DetailView

from .models import Post


def index(request):
    posts = Post.objects.order_by('-date_posted')
    return render(request, "home/index.html", context={"posts": posts})


class PostDetail(DetailView):
    model = Post
    template_name = "home/post_detail.html"
