# Generated by Django 5.0.3 on 2024-08-28 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0046_alter_game_player_game_stats_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="player_game_stats",
        ),
        migrations.RemoveField(
            model_name="game",
            name="team_game_stats",
        ),
    ]
