# Generated by Django 5.0.3 on 2024-06-23 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_rename_created_at_paymentlog_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentlog',
            name='user',
        ),
        migrations.RemoveField(
            model_name='upgradelog',
            name='user',
        ),
    ]
