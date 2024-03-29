# Generated by Django 4.1.4 on 2023-01-17 09:14

import accounts.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=240)),
                (
                    "description",
                    models.TextField(
                        default="A new channel on Tsuna Streaming.", max_length=500
                    ),
                ),
                (
                    "profile",
                    models.ImageField(
                        default="media/images/default-channel-profile.jpg",
                        upload_to="channels/profile",
                        validators=[accounts.validators.validate_profile_size],
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        default="media/images/default-thumbnail.jpg",
                        upload_to="channels/profile",
                        validators=[accounts.validators.validate_profile_size],
                    ),
                ),
                ("token", models.CharField(max_length=32)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channels",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
