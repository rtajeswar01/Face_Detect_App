# Generated by Django 4.2.5 on 2023-09-29 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='scheduleCode',
        ),
    ]
