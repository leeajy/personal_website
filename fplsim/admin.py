from django.contrib import admin
from .models import Player
from .models import Matchweek
from .models import Position
from .models import Team

# Register your models here.
admin.site.register(Player)
admin.site.register(Matchweek)
admin.site.register(Position)
admin.site.register(Team)