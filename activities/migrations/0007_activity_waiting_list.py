# Generated by Django 3.2.13 on 2022-06-28 16:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0006_activity_waiting_list_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='waiting_list',
            field=models.ManyToManyField(related_name='waiting_list', to=settings.AUTH_USER_MODEL),
        ),
    ]