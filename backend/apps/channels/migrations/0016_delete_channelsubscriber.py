# Generated by Django 4.1.4 on 2023-03-24 09:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("channels", "0015_alter_channelsubscriber_channel_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ChannelSubscriber",
        ),
    ]
