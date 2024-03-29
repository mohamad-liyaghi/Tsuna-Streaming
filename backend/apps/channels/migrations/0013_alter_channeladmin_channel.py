# Generated by Django 4.1.4 on 2023-02-20 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("channels", "0012_channeladmin_unique_channel_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channeladmin",
            name="channel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="admin",
                to="channels.channel",
            ),
        ),
    ]
