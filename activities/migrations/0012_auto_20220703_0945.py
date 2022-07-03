# Generated by Django 3.2.13 on 2022-07-03 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0011_auto_20220703_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='score',
        ),
        migrations.AlterField(
            model_name='activity',
            name='votes',
            field=models.ManyToManyField(blank=True, related_name='activities_voted', to='activities.ActivityVote'),
        ),
        migrations.AlterField(
            model_name='activityvote',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
    ]