from django.contrib import admin

from .models import Activity, Category, ActivityVote

admin.site.register(Activity)
admin.site.register(Category)
admin.site.register(ActivityVote)
