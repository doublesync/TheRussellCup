# Generated by Django 5.0.3 on 2024-08-24 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0031_alter_contractlog_current_year_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentlog",
            name="week",
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name="upgradelog",
            name="week",
            field=models.IntegerField(default=2),
        ),
    ]
