# Generated by Django 3.2.13 on 2022-07-02 13:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0009_alter_activity_waiting_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='score',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='activity',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activity',
            name='max_n_participants',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='activity',
            name='participants',
            field=models.ManyToManyField(related_name='activities', to=settings.AUTH_USER_MODEL),
        ),
    ]