# Generated by Django 4.1.4 on 2023-02-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0019_alter_plan_token_alter_subscription_token_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="token",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="token",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="token",
            name="token",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]