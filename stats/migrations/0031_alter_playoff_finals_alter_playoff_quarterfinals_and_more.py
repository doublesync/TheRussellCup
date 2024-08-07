# Generated by Django 5.0.3 on 2024-07-30 04:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0030_rename_round_3_playoff_finals_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playoff",
            name="finals",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="finals",
                to="stats.playoffround",
            ),
        ),
        migrations.AlterField(
            model_name="playoff",
            name="quarterfinals",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="quarterfinals",
                to="stats.playoffround",
            ),
        ),
        migrations.AlterField(
            model_name="playoff",
            name="semifinals",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="semifinals",
                to="stats.playoffround",
            ),
        ),
    ]
