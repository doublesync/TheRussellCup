# Generated by Django 5.0.3 on 2024-07-04 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_remove_game_away_team_player_stats_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='away_team_stats',
        ),
        migrations.RemoveField(
            model_name='game',
            name='home_team_stats',
        ),
    ]