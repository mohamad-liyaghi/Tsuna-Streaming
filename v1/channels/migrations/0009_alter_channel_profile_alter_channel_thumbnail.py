# Generated by Django 4.1.4 on 2023-02-10 09:40

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0008_channeladmin_block_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='profile',
            field=models.ImageField(default='assets/images/default-channel-profile.jpg', upload_to='channels/profile', validators=[accounts.validators.validate_profile_size]),
        ),
        migrations.AlterField(
            model_name='channel',
            name='thumbnail',
            field=models.ImageField(default='assets/images/default-thumbnail.jpg', upload_to='channels/profile', validators=[accounts.validators.validate_profile_size]),
        ),
    ]
