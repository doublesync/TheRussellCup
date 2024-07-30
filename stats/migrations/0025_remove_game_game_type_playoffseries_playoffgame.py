# Generated by Django 5.0.3 on 2024-07-30 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0024_season_current_storylines"),
        ("teams", "0006_team_surge"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="game_type",
        ),
        migrations.CreateModel(
            name="PlayoffSeries",
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
                (
                    "round",
                    models.CharField(
                        choices=[
                            ("Play-In Tournament", "Play-In Tournament"),
                            ("Conference Quarterfinals", "Conference Quarterfinals"),
                            ("Conference Finals", "Conference Finals"),
                            ("TRC Finals", "TRC Finals"),
                        ],
                        max_length=50,
                    ),
                ),
                ("team_a_seed", models.IntegerField()),
                ("team_b_seed", models.IntegerField()),
                ("wins_to_advance", models.IntegerField(default=5)),
                (
                    "season",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stats.season"
                    ),
                ),
                (
                    "team_a",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_a",
                        to="teams.team",
                    ),
                ),
                (
                    "team_b",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_b",
                        to="teams.team",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="series_winner",
                        to="teams.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayoffGame",
            fields=[
                (
                    "game_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="stats.game",
                    ),
                ),
                ("game_number", models.IntegerField()),
                (
                    "series",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stats.playoffseries",
                    ),
                ),
            ],
            bases=("stats.game",),
        ),
    ]
