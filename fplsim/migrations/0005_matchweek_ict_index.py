# Generated by Django 3.1.2 on 2020-10-21 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fplsim', '0004_team_abbrev'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchweek',
            name='ICT_index',
            field=models.FloatField(default=0),
        ),
    ]
