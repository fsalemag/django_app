from django.urls import path
from .views import ActivityView, CategoryView, ActivityDetailView, ActivityEditDetailView, ActivityCreateView

urlpatterns = [
    path("", ActivityView.as_view(), name="activities-index"),
    path("create", ActivityCreateView.as_view(), name='activities-create'),

    path("category/", CategoryView.as_view(), name="activities-categories"),
    path("category/<category>", ActivityView.as_view(), name='activities-category'),
    path("category/<category>/<pk>", ActivityDetailView.as_view(), name='activities-detail'),
    path("category/<category>/<pk>/edit", ActivityEditDetailView.as_view(), name='activities-edit-detail'),
]
