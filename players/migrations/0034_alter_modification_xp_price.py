# Generated by Django 5.0.3 on 2024-07-28 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0033_alter_player_coach_suggestion_attributes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="modification",
            name="xp_price",
            field=models.IntegerField(default=0),
        ),
    ]