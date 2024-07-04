# Generated by Django 5.0.3 on 2024-07-04 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0009_remove_game_away_team_stats_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
