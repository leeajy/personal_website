from django.core.management.base import BaseCommand, CommandError
from fplsim.models import Player, Matchweek, Team, Position
from django.core.files.storage import default_storage
from django.conf import settings
import os, csv


class Command(BaseCommand):
    help = 'Extracts data for any of the models in the Fplsim application'

    def add_arguments(self, parser):
        parser.add_argument('models', nargs='+', type=str)

    def handle(self, *args, **options):
        for model in options['models']:
            try:
                model = model.lower()
                if model == 'player':
                    self.playerETL()
                elif model == 'matchweek':
                    self.matchweekETL()
                elif model == 'team':
                    self.teamETL()
                elif model == 'position':
                    self.positionETL()
                else:
                    raise CommandError('Model %s does not exist' % model)
            except Exception as inst:
                raise CommandError('Error occurred. %s' % inst)

            self.stdout.write(self.style.SUCCESS('Successfully loaded %s' % model))

    def positionETL(self):
        if len(Position.objects.all()) != 4:
            Position(id=1, name='Goalkeeper').save()
            Position(id=2, name='Defender').save()
            Position(id=3, name='Midfielder').save()
            Position(id=4, name='Forward').save()
        else:
            self.stdout.write(self.style.SUCCESS('No new data loaded - position '))

    def playerETL(self):
        storage_path = getattr(settings, 'MEDIA_ROOT', None)
        # django storage version
        # book = default_storage.open(os.path.join(storage_path, '2017-18/player_idlist.csv'), 'r')
        with open(os.path.join(storage_path, '2017-18/player_idlist.csv'), encoding="utf8") as playercsv:
            data = csv.reader(playercsv, delimiter=',')
            next(data)  # ignore first row as it is column titles
            for row in data:
                Player(id=row[2], first_name=row[0], last_name=row[1],
                       position=Position.objects.get(id=int(row[3])),
                       team=Team.objects.get(id=int(row[4])),
                       value=float(row[5])).save()
                # print(', '.join(row))

    def matchweekETL(self):
        storage_path = getattr(settings, 'MEDIA_ROOT', None)
        # django storage version
        # book = default_storage.open(os.path.join(storage_path, '2017-18/player_idlist.csv'), 'r')
        for i in range(1, 8):
            try:
                with open(os.path.join(storage_path, '2017-18/gws/gw' + str(i) + '.csv')) as matchweekcsv:
                    data = csv.reader(matchweekcsv, delimiter=',')
                    next(data)  # ignore first row as it is column titles
                    for row in data:
                        try:
                            currPlayer = Player.objects.get(id=row[13])
                            Matchweek(player=currPlayer, round=i, goals=row[19],
                                      assists=row[1], minutes=row[29], clean_sheets=row[7],
                                      yellow_cards=row[54], red_cards=row[37], total_points=row[47],
                                      ICT_index=row[20]).save()
                        except Exception as inst:
                            print(f'skipped for {row[0]} for matchweek {i}. Exception: {inst}')
            except Exception as inst:
                print(f'skipped row in gameweek {i}. Exception: {inst}')


    def teamETL(self):
        storage_path = getattr(settings, 'MEDIA_ROOT', None)
        with open(os.path.join(storage_path, '2017-18/teams_raw.csv'), encoding="utf8") as teamcsv:
            data = csv.reader(teamcsv, delimiter=',')
            next(data)  # ignore first row as it is column titles
            for row in data:
                Team(id=row[1], name=row[2], abbrev=row[3]).save()
