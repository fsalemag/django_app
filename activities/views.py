from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView

from users.models import UserProfile
from .forms import ActivityForm
from .models import Activity, Category, ActivityVote


class CategoryView(ListView):
    model = Category
    template_name = "activities/index.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(n_activities=Count('category_activity')).order_by(
            "-n_activities"
        )

        return qs


class ActivityView(ListView):
    model = Activity
    template_name = "activities/activities.html"

    def get_queryset(self):
        GET = self.request.GET
        qs = super().get_queryset()
        if self.kwargs.get("category"):
            qs = qs.filter(category__name=self.kwargs["category"])

        if GET.get("max_participants"):
            qs = qs.filter(max_n_participants__lte=GET.get("max_participants"))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs.get("category")

        return context

    # ordering = ['-date_posted']


class ActivityDetailView(DetailView):
    model = Activity
    template_name = "activities/activity-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participants = context["activity"].participants.all()
        context["profiles"] = UserProfile.objects.filter(user__in=participants)

        votes = context["activity"].votes.all()
        context["voters"] = votes.values_list("voter", flat=True)
        return context

    # ordering = ['-date_posted']


class ActivityCreateView(CreateView):
    model = Activity
    template_name = "activities/create-activity.html"

    fields = [
        'title', 'description', 'location', 'time_of_event', 'max_n_participants', 'category'
    ]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()

        return redirect(reverse('users-activities'))

    # ordering = ['-date_posted']


class ActivityEditDetailView(UpdateView):
    model = Activity
    template_name = "activities/edit-activity-detail.html"
    # fields = [
    #     'title', 'description', 'location', 'time_of_event'
    # ]

    form_class = ActivityForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.get_object().creator.email == request.user.email:
                return super().get(request, *args, **kwargs)
            else:
                return redirect("home-index")
        else:
            return redirect("account_login")

    def post(self, request, *args, **kwargs):
        activity = Activity.objects.get(pk=kwargs["pk"])

        # Remove logged user from the current activity
        if request.POST.get("action", "") == "unjoin":
            activity.participants.remove(request.user)
            return redirect(reverse("activities-detail", kwargs=kwargs), permanent=True)

        # Add logged in user to the current activity
        elif request.POST.get("action", "") == "join":
            activity.participants.add(request.user)
            return redirect(reverse("activities-detail", kwargs=kwargs), permanent=True)

        if request.POST.get("action", "") == "unjoin-waiting-list":
            activity.waiting_list.remove(request.user)
            return redirect(reverse("activities-detail", kwargs=kwargs), permanent=True)

        # Add logged in user to the current activity
        elif request.POST.get("action", "") == "join-waiting-list":
            activity.waiting_list.add(request.user)
            return redirect(reverse("activities-detail", kwargs=kwargs), permanent=True)

        # Add vote
        elif request.POST.get("action", "") == "vote":
            vote = ActivityVote.objects.create(
                voter=self.request.user,
                score=request.POST.get("score")
            )
            activity.votes.add(vote)
            return redirect(reverse("activities-detail", kwargs=kwargs), permanent=True)

        # Normal form to update activity with self.fields
        else:
            return super().post(request, *args, **kwargs)
