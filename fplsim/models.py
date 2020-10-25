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


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

    def name(self):
        # if they have more than one first name or last name, only use first
        first = self.first_name.split(' ')[0]
        last = self.last_name.split(' ')[0:2]
        return first + ' ' + ' '.join(last)

    def __str__(self):
        return self.first_name[0] + '. ' + self.last_name + ' ; ' + self.team.__str__() + \
               ' ; $' + str(self.value)


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


class Tweet(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    sentiment = models.FloatField(default=0)
    round = models.IntegerField()

    def __str__(self):
        return '{0}'.format(self.text)

class Result(models.Model):
    points = models.IntegerField()
    scraping_level = models.IntegerField()
    cost = models.FloatField()

    def resultType(self):
        if self.scraping_level == 0:
            return 'Form based'
        elif self.scraping_level == 1:
            return 'Sentiment based'
        elif self.scraping_level == -1:
            return 'Control'

    def __str__(self):
        return 'Points: {0:d}, Cost:{1:.2f}, Type:{2}'.format(self.points,
                                                              self.cost,
                                                              self.resultType())
