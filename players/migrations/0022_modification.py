# Generated by Django 5.0.3 on 2024-06-30 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0021_player_on_roster'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=64)),
                ('xp_price', models.IntegerField()),
                ('sp_price', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
