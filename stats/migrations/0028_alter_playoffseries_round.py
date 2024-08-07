# Generated by Django 5.0.3 on 2024-07-30 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0027_alter_playoffseries_round"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playoffseries",
            name="round",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="stats.playoffround",
            ),
            preserve_default=False,
        ),
    ]
