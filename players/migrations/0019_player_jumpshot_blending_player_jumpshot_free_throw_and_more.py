# Generated by Django 5.0.3 on 2024-06-27 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0018_alter_player_svg_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='jumpshot_blending',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='player',
            name='jumpshot_free_throw',
            field=models.CharField(default='N/A', max_length=32),
        ),
        migrations.AddField(
            model_name='player',
            name='jumpshot_release_1',
            field=models.CharField(default='N/A', max_length=32),
        ),
        migrations.AddField(
            model_name='player',
            name='jumpshot_release_2',
            field=models.CharField(default='N/A', max_length=32),
        ),
    ]
