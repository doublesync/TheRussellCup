# Generated by Django 5.0.3 on 2024-12-11 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0041_alter_paymentlog_season_alter_paymentlog_week_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentlog',
            name='week',
            field=models.IntegerField(default=9),
        ),
        migrations.AlterField(
            model_name='upgradelog',
            name='week',
            field=models.IntegerField(default=9),
        ),
    ]
