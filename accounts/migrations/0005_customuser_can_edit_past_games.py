# Generated by Django 5.0.3 on 2024-07-18 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_customuser_can_edit_stats"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="can_edit_past_games",
            field=models.BooleanField(default=False),
        ),
    ]
