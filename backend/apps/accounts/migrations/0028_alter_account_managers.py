# Generated by Django 4.1.4 on 2023-07-16 09:33

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0027_alter_account_token_alter_token_token"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="account",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]