# Generated by Django 5.0.3 on 2024-06-20 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0010_alter_player_tendencies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='sim_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
