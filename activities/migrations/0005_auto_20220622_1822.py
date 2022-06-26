# Generated by Django 3.2.13 on 2022-06-22 18:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0004_auto_20220622_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='n_participants',
        ),
        migrations.AddField(
            model_name='activity',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]