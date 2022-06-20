from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import UserProfile

class ProfileView(View):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        return render(request, "users/profile.html", context={"user_profile": user_profile})
