from django.db import models
# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=100)
    # content = models.TextField() unrestricted text
    # date = models.DateTimeField(default = timezone.now)
    position = None  # make an enumeration for GK, DEF, MID, OFF
    team = None  # make an enumeration for team

    def __str__(self):
        return Player.name


class Matchweek(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    round = models.IntegerField()

    def __str__(self):
        return 'Matchweek {0!s}, player {1}, total_points: {2!s}'.format(self.round,
                                                                         self.player.name,
                                                                         self.total_points)
