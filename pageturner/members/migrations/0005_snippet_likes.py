# Generated by Django 4.2.5 on 2023-10-07 04:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0004_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='snippet_like', to=settings.AUTH_USER_MODEL),
        ),
    ]