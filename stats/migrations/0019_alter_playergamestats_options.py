# Generated by Django 5.0.3 on 2024-07-17 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "stats",
            "0018_alter_playergamestats_effective_field_goal_percentage_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="playergamestats",
            options={"get_latest_by": "game_score"},
        ),
    ]
