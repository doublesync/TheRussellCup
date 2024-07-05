# Generated by Django 5.0.3 on 2024-07-05 21:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0017_alter_contractlog_option'),
        ('players', '0028_player_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractlog',
            name='player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='players.player'),
            preserve_default=False,
        ),
    ]