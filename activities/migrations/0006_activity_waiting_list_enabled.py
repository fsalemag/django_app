# Generated by Django 3.2.13 on 2022-06-28 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20220622_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='waiting_list_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
