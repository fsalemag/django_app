from django.urls import path
from .views import ProfileView, ProfileActivityView

urlpatterns = [
        path("", ProfileView.as_view(), name="users-profile"),
        path("activities", ProfileActivityView.as_view(), name="users-activities"),
        path("<pk>", ProfileView.as_view(), name="users-external-profile"),
]
