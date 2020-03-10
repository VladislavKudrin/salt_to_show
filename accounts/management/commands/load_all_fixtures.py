from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.management import call_command

FIXTURES = [
		'admin',
		'brands',
		'regions',
		'categories'
		]

class Command(BaseCommand):
    help = 'Loads our fixtures'

    def handle(self, *args, **kwargs):
    	for fixture in FIXTURES:
        	call_command('loaddata', fixture)
