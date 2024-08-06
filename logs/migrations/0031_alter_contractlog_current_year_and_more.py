# Generated by Django 5.0.3 on 2024-08-06 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "logs",
            "0030_rename_current_year_payment_contractlog_year_1_payment_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="contractlog",
            name="current_year",
            field=models.CharField(
                choices=[
                    ("Year 1", "Year 1"),
                    ("Year 2", "Year 2"),
                    ("Year 3", "Year 3"),
                ],
                default="Year 1",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="paymentlog",
            name="season",
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name="paymentlog",
            name="week",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="upgradelog",
            name="season",
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name="upgradelog",
            name="week",
            field=models.IntegerField(default=0),
        ),
    ]
