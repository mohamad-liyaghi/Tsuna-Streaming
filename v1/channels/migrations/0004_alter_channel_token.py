# Generated by Django 4.1.4 on 2023-01-17 09:32

import channels.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0003_alter_channel_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='token',
            field=models.CharField(default=channels.utils.channel_token_generator, max_length=32, unique=True),
        ),
    ]