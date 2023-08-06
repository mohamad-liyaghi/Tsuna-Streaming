# Generated by Django 4.1.4 on 2023-08-06 10:15

import contents.models.utils.thumbnail_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0010_alter_video_file_alter_video_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(default='static/images/default-thumbnail.jpg', upload_to=contents.models.utils.thumbnail_path.get_thumbnail_upload_path),
        ),
    ]
