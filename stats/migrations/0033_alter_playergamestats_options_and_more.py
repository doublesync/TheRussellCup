# Generated by Django 5.0.3 on 2024-07-30 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0032_remove_playoffseries_wins_to_advance_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="playergamestats",
            options={"verbose_name_plural": "Player game stats"},
        ),
        migrations.AlterModelOptions(
            name="playoffseries",
            options={"verbose_name_plural": "Playoff series"},
        ),
        migrations.AlterModelOptions(
            name="teamgamestats",
            options={"verbose_name_plural": "Team game stats"},
        ),
        migrations.RemoveField(
            model_name="playoffseries",
            name="season",
        ),
    ]