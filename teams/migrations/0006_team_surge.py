# Generated by Django 5.0.3 on 2024-07-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0005_alter_draft_season"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="surge",
            field=models.BooleanField(default=False),
        ),
    ]
