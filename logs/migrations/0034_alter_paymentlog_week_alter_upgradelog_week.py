# Generated by Django 5.0.3 on 2024-08-24 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0033_alter_paymentlog_week_alter_upgradelog_week"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentlog",
            name="week",
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name="upgradelog",
            name="week",
            field=models.IntegerField(default=4),
        ),
    ]
