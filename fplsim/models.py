from django.db import models


# Create your models here.
class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Position(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# source - players_raw.csv
class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name[0] + '. ' + self.last_name


class Matchweek(models.Model):
    round = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    ICT_index = models.FloatField(default=0)

    def __str__(self):
        return 'Matchweek: {0!s}, Player: {1}, Total Points: {2!s}'.format(self.round,
                                                                         self.player,
                                                                         self.total_points)
