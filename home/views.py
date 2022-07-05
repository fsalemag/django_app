from datetime import timedelta

from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from activities.models import Activity, Category
from users.models import MyUser


def index(request):
    n_activities = Activity.objects.all().count()
    n_users = MyUser.objects.all().count()
    top_categories = Category.objects.all().annotate(count=Count("category_activity")).order_by("-count")[:3]
    n_month_activities = Activity.objects.filter(created_on__gte=timezone.now() - timedelta(days=30)).count()

    trending_categories = Category.objects.filter(
        category_activity__created_on__gte=timezone.now() - timedelta(days=7)).annotate(
        count=Count("category_activity")).order_by("-count")[:3]

    return render(
        request,
        "home/index.html",
        context={
            "n_activities": n_activities,
            "n_users": n_users,
            "top_categories": top_categories,
            "n_month_activities": n_month_activities,
            "trending_categories": trending_categories
        }
    )
