# Generated by Django 4.1.4 on 2023-01-12 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0009_alter_plan_active_months_alter_plan_description_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plan",
            name="is_avaiable",
        ),
        migrations.AddField(
            model_name="plan",
            name="is_available",
            field=models.BooleanField(default=False),
        ),
    ]
