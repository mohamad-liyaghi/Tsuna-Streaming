# Generated by Django 4.1.4 on 2023-07-16 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_alter_account_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='role',
        ),
    ]