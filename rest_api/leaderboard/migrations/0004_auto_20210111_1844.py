# Generated by Django 3.1.5 on 2021-01-11 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0003_auto_20210111_1818'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClassMeeting',
        ),
        migrations.DeleteModel(
            name='School',
        ),
    ]