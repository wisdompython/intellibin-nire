# Generated by Django 5.0.4 on 2024-08-07 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_rename_wastebinrequests_wastebinrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wastebinrequest',
            name='date_delivered',
        ),
        migrations.RemoveField(
            model_name='wastebinrequest',
            name='delivered',
        ),
    ]