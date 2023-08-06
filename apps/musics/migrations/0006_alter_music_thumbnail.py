# Generated by Django 4.1.4 on 2023-08-06 10:19

import contents.models.utils.thumbnail_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0005_alter_music_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='thumbnail',
            field=models.ImageField(default='assets/images/default-thumbnail.jpg', upload_to=contents.models.utils.thumbnail_path.get_thumbnail_upload_path),
        ),
    ]
