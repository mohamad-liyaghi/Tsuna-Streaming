# Generated by Django 4.1.4 on 2023-08-06 10:15

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0032_alter_verificationtoken_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="picture",
            field=models.ImageField(
                default="static/images/default-user-profile.jpg",
                upload_to="accounts/profile",
                validators=[accounts.validators.validate_profile_size],
            ),
        ),
    ]