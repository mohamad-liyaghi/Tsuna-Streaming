# Generated by Django 4.1.4 on 2023-02-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0002_alter_video_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="allow_comment",
            field=models.BooleanField(default=True),
        ),
    ]
