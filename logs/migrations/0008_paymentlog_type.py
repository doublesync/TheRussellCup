# Generated by Django 5.0.3 on 2024-06-27 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007_paymentlog_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentlog',
            name='type',
            field=models.CharField(choices=[('SP', 'SP'), ('XP', 'XP')], default=1, max_length=2),
            preserve_default=False,
        ),
    ]
