# Generated by Django 4.1.4 on 2023-03-14 11:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0022_remove_subscription_plan_remove_subscription_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Plan",
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
                ("title", models.CharField(max_length=210)),
                (
                    "description",
                    models.TextField(
                        default="No Description available", max_length=400
                    ),
                ),
                (
                    "price",
                    models.PositiveBigIntegerField(
                        default=10,
                        validators=[
                            django.core.validators.MaxValueValidator(1000),
                            django.core.validators.MinValueValidator(10),
                        ],
                    ),
                ),
                ("token", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "active_months",
                    models.PositiveBigIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(24),
                            django.core.validators.MinValueValidator(1),
                        ],
                    ),
                ),
                ("is_available", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
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
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("finish_date", models.DateTimeField(blank=True, null=True)),
                ("token", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plans",
                        to="accounts.plan",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
