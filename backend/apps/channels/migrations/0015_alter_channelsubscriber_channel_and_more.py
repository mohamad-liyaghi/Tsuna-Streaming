# Generated by Django 4.1.4 on 2023-03-16 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("channels", "0014_delete_channeladmin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channelsubscriber",
            name="channel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscriber",
                to="channels.channel",
            ),
        ),
        migrations.AlterField(
            model_name="channelsubscriber",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscribed_channel",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
