# Generated by Django 5.0.3 on 2024-06-19 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='anomaly',
            field=models.BooleanField(default=False),
        ),
    ]
