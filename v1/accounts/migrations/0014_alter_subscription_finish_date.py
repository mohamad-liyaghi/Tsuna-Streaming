# Generated by Django 4.1.4 on 2023-01-14 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_subscription_finish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
