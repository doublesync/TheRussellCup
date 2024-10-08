# Generated by Django 5.0.3 on 2024-08-26 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0034_playerseasonstats"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="playerseasonstats",
            options={"verbose_name_plural": "Player season stats"},
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_assists",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_blocks",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_defensive_rebounds",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_dunks",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_effective_field_goal_percentage",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_field_goals_attempted",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_field_goals_made",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_free_throws_attempted",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_free_throws_made",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_game_score",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_offensive_rebounds",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_personal_fouls",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_plus_minus",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_points_responsible_for",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_rebounds",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_steals",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_three_pointers_attempted",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_three_pointers_made",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_true_shooting_percentage",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_turnover_percentage",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="playerseasonstats",
            name="game_high_turnovers",
            field=models.IntegerField(default=0),
        ),
    ]
