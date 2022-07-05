from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView
from django.views.generic import View

from .models import UserProfile


class ProfileView(View):
    def get(self, request, pk=None):
        if not pk:
            user = request.user
            if not user.is_authenticated:
                return redirect(reverse('account_login'))

            user_profile = UserProfile.objects.get(user=user)
        else:
            user_profile = UserProfile.objects.get(pk=pk)

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
