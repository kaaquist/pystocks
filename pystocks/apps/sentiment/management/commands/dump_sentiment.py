from django.core.management.base import BaseCommand
from pystocks.apps.sentiment import dumper

class Command(BaseCommand):

    def handle(self, *args, **options):
        dumper.dump_all()