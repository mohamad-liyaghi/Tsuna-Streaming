# Generated by Django 4.1.4 on 2023-07-15 11:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0005_alter_comment_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
