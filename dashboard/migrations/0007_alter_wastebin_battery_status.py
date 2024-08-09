# Generated by Django 5.0.4 on 2024-08-08 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_wastebin_battery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wastebin',
            name='battery_status',
            field=models.CharField(choices=[('FULL', 'FULL'), ('LOW', 'LOW'), ('OKAY', 'OKAY')], default=None, max_length=20, null=True),
        ),
    ]
