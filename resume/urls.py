from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="resume-index"),
        path("download", views.download, name="resume-download"),
]