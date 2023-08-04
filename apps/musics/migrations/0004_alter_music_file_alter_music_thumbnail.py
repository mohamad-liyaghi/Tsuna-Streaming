# Generated by Django 4.1.4 on 2023-08-04 09:31

import contents.models.utils.file_path
import contents.models.utils.thumbnail_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0003_remove_music_music_music_file_alter_music_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='file',
            field=models.FileField(upload_to=contents.models.utils.file_path.get_file_upload_path),
        ),
        migrations.AlterField(
            model_name='music',
            name='thumbnail',
            field=models.ImageField(default='assets/images/default-thumbnail.jpg', upload_to=contents.models.utils.thumbnail_path.get_thumbnail_upload_path),
        ),
    ]
