# Generated by Django 4.0.5 on 2022-07-03 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0012_auto_20220703_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='votes',
            field=models.ManyToManyField(blank=True, null=True, related_name='activities_voted', to='activities.activityvote'),
        ),
    ]
