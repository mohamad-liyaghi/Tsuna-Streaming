# Generated by Django 4.1.4 on 2023-07-15 13:52

import apps.contents.models.utils.file_path
import apps.contents.models.utils.thumbnail_path
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0008_alter_video_token"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="video",
            name="video",
        ),
        migrations.AddField(
            model_name="video",
            name="file",
            field=models.FileField(
                default="22",
                upload_to=apps.contents.models.utils.file_path.get_file_upload_path,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="video",
            name="thumbnail",
            field=models.ImageField(
                default="assets/images/default-thumbnail.jpg",
                upload_to=apps.contents.models.utils.thumbnail_path.get_thumbnail_upload_path,
            ),
        ),
    ]