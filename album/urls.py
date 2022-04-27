from django.urls import path
from . import views

urlpatterns = [
        path("", views.Album.as_view(), name="album-index"),
]
