# Generated by Django 4.1.4 on 2023-01-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0011_subscription"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="start_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
