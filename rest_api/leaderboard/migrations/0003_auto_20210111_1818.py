# Generated by Django 3.1.5 on 2021-01-11 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0002_auto_20210111_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classmeeting',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leaderboard.school'),
        ),
    ]
