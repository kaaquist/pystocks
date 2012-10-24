from django.core.management.base import BaseCommand
from pystocks.collector import collector

class Command(BaseCommand):

    def handle(self, *args, **options):
        collector.collect()