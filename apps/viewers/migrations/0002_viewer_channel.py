# Generated by Django 4.1.4 on 2023-07-30 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0019_rename_profile_channel_avatar_and_more'),
        ('viewers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewer',
            name='channel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='channels.channel'),
        ),
    ]
