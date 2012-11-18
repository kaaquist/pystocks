from django.core.management.base import BaseCommand
from pystocks.apps.collector import collector

class Command(BaseCommand):

    def handle(self, *args, **options):
        collector.collect()
