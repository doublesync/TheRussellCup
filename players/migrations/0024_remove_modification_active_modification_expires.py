# Generated by Django 5.0.3 on 2024-06-30 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0023_player_modifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modification',
            name='active',
        ),
        migrations.AddField(
            model_name='modification',
            name='expires',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
