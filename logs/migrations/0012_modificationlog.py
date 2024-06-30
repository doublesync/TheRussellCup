# Generated by Django 5.0.3 on 2024-06-30 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0011_upgradelog_complete'),
        ('players', '0022_modification'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModificationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(default=1)),
                ('season', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.modification')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
            ],
        ),
    ]
