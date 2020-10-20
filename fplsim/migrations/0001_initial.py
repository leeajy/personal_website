# Generated by Django 3.1.2 on 2020-10-20 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Matchweek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goals', models.IntegerField(default=0)),
                ('assists', models.IntegerField(default=0)),
                ('minutes', models.IntegerField(default=0)),
                ('clean_sheets', models.IntegerField(default=0)),
                ('yellow_cards', models.IntegerField(default=0)),
                ('red_cards', models.IntegerField(default=0)),
                ('total_points', models.IntegerField(default=0)),
                ('round', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fplsim.player')),
            ],
        ),
    ]
