from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .models import Activity, Category


class CategoryView(ListView):
    model = Category
    template_name = "activities/index.html"
    # ordering = ['-date_posted']


class ActivityView(ListView):
    model = Activity
    template_name = "activities/activities.html"
    # ordering = ['-date_posted']


class ActivityDetailView(DetailView):
    model = Activity
    template_name = "activities/activity-detail.html"
    # ordering = ['-date_posted']


class ActivityEditDetailView(UpdateView):
    model = Activity
    template_name = "activities/edit-activity-detail.html"
    fields = [
        'title', 'description', 'location', 'time_of_event'
    ]

    def get(self, request, *args, **kwargs):
        print(dir(self.get_object()))
        # if self.get_object().get(email=user == request.user.email:
        #     return super().get(request, *args, **kwargs)
        # else:
        #     print("welele")
        return super().get(request, *args, **kwargs)
