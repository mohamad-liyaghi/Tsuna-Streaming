# Generated by Django 4.1.4 on 2023-03-16 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('channel_admins', '0007_channeladmin_channeladminpermission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeladmin',
            name='promoted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promoted_admins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channeladmin',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channel_admins', to=settings.AUTH_USER_MODEL),
        ),
    ]
