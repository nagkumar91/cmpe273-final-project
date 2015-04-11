from django.core.management import BaseCommand
from core.models import TweetMasterData as TMD, AppUser
__author__ = 'nagkumar'


class Command(BaseCommand):
    help = "Dumps dummy data to the log"

    def handle(self, *args, **options):
        TMD.objects.all().delete()
