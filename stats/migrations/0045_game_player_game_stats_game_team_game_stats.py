# Generated by Django 5.0.3 on 2024-08-28 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0044_remove_teamseasonstats_average_plus_minus_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="player_game_stats",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="player_game_stats",
                to="stats.playergamestats",
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="team_game_stats",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="team_game_stats",
                to="stats.teamgamestats",
            ),
        ),
    ]
