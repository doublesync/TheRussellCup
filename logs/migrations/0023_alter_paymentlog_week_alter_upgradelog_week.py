# Generated by Django 5.0.3 on 2024-07-18 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0022_alter_paymentlog_week_alter_upgradelog_week"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentlog",
            name="week",
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name="upgradelog",
            name="week",
            field=models.IntegerField(default=12),
        ),
    ]
