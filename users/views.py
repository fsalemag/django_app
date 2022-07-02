from django.shortcuts import render
from django.views.generic import View
from django.views.generic import DetailView


from .models import UserProfile


class ProfileView(View):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        return render(
            request,
            "users/profile.html",
            context={
                "user_profile": user_profile,
            }
        )


class ProfileActivityView(DetailView):
    model = UserProfile
    template_name = "users/activities.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)

        return qs

    def get_object(self, queryset=None):
        qs = self.get_queryset()
        return qs.get()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = context.pop("object")

        # Joined activities

        # To join activities

        # My activities
        print(context)
        return context
