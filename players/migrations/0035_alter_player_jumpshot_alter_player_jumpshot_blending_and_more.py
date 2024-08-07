# Generated by Django 5.0.3 on 2024-08-05 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0034_alter_modification_xp_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="jumpshot",
            field=models.CharField(blank=True, default="N/A", max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="jumpshot_blending",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="jumpshot_free_throw",
            field=models.CharField(blank=True, default="N/A", max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="jumpshot_release_1",
            field=models.CharField(blank=True, default="N/A", max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="jumpshot_release_2",
            field=models.CharField(blank=True, default="N/A", max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="jumpshot_timing",
            field=models.CharField(blank=True, default="N/A", max_length=32, null=True),
        ),
    ]
