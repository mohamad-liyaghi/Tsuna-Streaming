# Generated by Django 4.1.4 on 2023-01-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.CharField(blank=True, null=True, max_length=32),
        ),
    ]
