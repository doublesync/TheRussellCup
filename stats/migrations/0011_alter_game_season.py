# Generated by Django 5.0.3 on 2024-07-04 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.season'),
        ),
    ]
