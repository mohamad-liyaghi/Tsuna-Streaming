# Generated by Django 4.1.4 on 2023-02-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0002_alter_comment_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="token",
            field=models.CharField(blank=True, null=True, max_length=32),
        ),
    ]
