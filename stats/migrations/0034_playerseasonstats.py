# Generated by Django 5.0.3 on 2024-08-26 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0037_modification_xp_price_with_discount"),
        ("stats", "0033_alter_playergamestats_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerSeasonStats",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("games_played", models.IntegerField(default=0)),
                ("minutes", models.IntegerField(default=0)),
                ("points", models.IntegerField(default=0)),
                ("rebounds", models.IntegerField(default=0)),
                ("assists", models.IntegerField(default=0)),
                ("steals", models.IntegerField(default=0)),
                ("blocks", models.IntegerField(default=0)),
                ("turnovers", models.IntegerField(default=0)),
                ("field_goals_made", models.IntegerField(default=0)),
                ("field_goals_attempted", models.IntegerField(default=0)),
                ("three_pointers_made", models.IntegerField(default=0)),
                ("three_pointers_attempted", models.IntegerField(default=0)),
                ("free_throws_made", models.IntegerField(default=0)),
                ("free_throws_attempted", models.IntegerField(default=0)),
                ("offensive_rebounds", models.IntegerField(default=0)),
                ("personal_fouls", models.IntegerField(default=0)),
                ("plus_minus", models.IntegerField(default=0)),
                ("points_responsible_for", models.IntegerField(default=0)),
                ("dunks", models.IntegerField(default=0)),
                ("defensive_rebounds", models.IntegerField(default=0)),
                ("game_score", models.FloatField(default=0.0)),
                ("effective_field_goal_percentage", models.FloatField(default=0.0)),
                ("true_shooting_percentage", models.FloatField(default=0.0)),
                ("turnover_percentage", models.FloatField(default=0.0)),
                ("average_minutes", models.FloatField(default=0.0)),
                ("average_points", models.FloatField(default=0.0)),
                ("average_rebounds", models.FloatField(default=0.0)),
                ("average_assists", models.FloatField(default=0.0)),
                ("average_steals", models.FloatField(default=0.0)),
                ("average_blocks", models.FloatField(default=0.0)),
                ("average_turnovers", models.FloatField(default=0.0)),
                ("average_field_goals_made", models.FloatField(default=0.0)),
                ("average_field_goals_attempted", models.FloatField(default=0.0)),
                ("average_three_pointers_made", models.FloatField(default=0.0)),
                ("average_three_pointers_attempted", models.FloatField(default=0.0)),
                ("average_free_throws_made", models.FloatField(default=0.0)),
                ("average_free_throws_attempted", models.FloatField(default=0.0)),
                ("average_offensive_rebounds", models.FloatField(default=0.0)),
                ("average_personal_fouls", models.FloatField(default=0.0)),
                ("average_plus_minus", models.FloatField(default=0.0)),
                ("average_points_responsible_for", models.FloatField(default=0.0)),
                ("average_dunks", models.FloatField(default=0.0)),
                ("average_defensive_rebounds", models.FloatField(default=0.0)),
                ("average_game_score", models.FloatField(default=0.0)),
                (
                    "average_effective_field_goal_percentage",
                    models.FloatField(default=0.0),
                ),
                ("average_true_shooting_percentage", models.FloatField(default=0.0)),
                ("average_turnover_percentage", models.FloatField(default=0.0)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="players.player"
                    ),
                ),
                (
                    "season",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stats.season"
                    ),
                ),
            ],
        ),
    ]