from django.urls import path

from . import views

urlpatterns = [
        path("", views.index, name="home-index"),
        path("<int:pk>", views.PostDetail.as_view(), name='home-post-detail')
]
