# Generated by Django 4.1.4 on 2023-02-20 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('channels', '0013_alter_channeladmin_channel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(blank=True, max_length=32, null=True)),
                ('change_channel_info', models.BooleanField(default=False)),
                ('add_new_admin', models.BooleanField(default=False)),
                ('block_user', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admins', to='channels.channel')),
                ('promoted_by', models.ForeignKey(on_delete=django.db.models.fields.CharField, related_name='promoted_admin', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='admin',
            constraint=models.UniqueConstraint(fields=('channel', 'user'), name='unique_channel_admins'),
        ),
    ]