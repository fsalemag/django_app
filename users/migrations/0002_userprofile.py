# Generated by Django 3.2.13 on 2022-06-20 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.myuser')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('f', 'Female'), ('m', 'Male'), ('o', 'Other')], max_length=1)),
                ('phone_number', models.IntegerField()),
            ],
            options={
                'verbose_name': 'UserProfile',
                'verbose_name_plural': 'UserProfiles',
            },
        ),
    ]
