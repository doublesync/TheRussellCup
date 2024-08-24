# Generated by Django 5.0.3 on 2024-08-24 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0036_rename_expired_modification_multi_buy"),
    ]

    operations = [
        migrations.AddField(
            model_name="modification",
            name="xp_price_with_discount",
            field=models.IntegerField(
                default=0, help_text="This is automatically calculated."
            ),
        ),
    ]