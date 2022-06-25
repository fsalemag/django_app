from django.urls import path
from .views import ActivityView, CategoryView, ActivityDetailView, ActivityEditDetailView, ActivityCreateView, \
    ActivityMineView

urlpatterns = [
    path("", CategoryView.as_view(), name="activities-index"),
    path("category/<category>", ActivityView.as_view(), name='activities-category'),
    path("category/<category>/<pk>", ActivityDetailView.as_view(), name='activities-detail'),
    path("category/<category>/<pk>/edit", ActivityEditDetailView.as_view(), name='activities-edit-detail'),
    path("create", ActivityCreateView.as_view(), name='activities-create'),
    path("create", ActivityCreateView.as_view(), name='activities-create'),
    path("mine", ActivityMineView.as_view(), name='activities-mine'),
]
