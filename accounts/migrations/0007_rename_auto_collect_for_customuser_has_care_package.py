# Generated by Django 5.0.3 on 2024-08-24 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_remove_customuser_can_edit_past_games_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="auto_collect_for",
            new_name="has_care_package",
        ),
    ]
