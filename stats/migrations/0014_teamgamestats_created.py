# Generated by Django 5.0.3 on 2024-07-15 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0013_playergamestats_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="teamgamestats",
            name="created",
            field=models.DateTimeField(auto_now_add=True, default="2024-07-15 14:49"),
            preserve_default=False,
        ),
    ]
