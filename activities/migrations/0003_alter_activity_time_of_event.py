# Generated by Django 3.2.13 on 2022-06-22 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20220622_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='time_of_event',
            field=models.DateTimeField(),
        ),
    ]
