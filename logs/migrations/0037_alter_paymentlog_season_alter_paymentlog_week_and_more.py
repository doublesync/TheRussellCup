# Generated by Django 5.0.3 on 2024-09-26 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0036_alter_paymentlog_week_alter_upgradelog_week"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentlog",
            name="season",
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="paymentlog",
            name="week",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="upgradelog",
            name="season",
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name="upgradelog",
            name="week",
            field=models.IntegerField(default=0),
        ),
    ]
