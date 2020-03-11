from django.core.management.base import BaseCommand
from django.core.management import call_command

FIXTURES = [
		'admin',
		'brands',
		'regions',
		'categories',
		]

class Command(BaseCommand):
    help = 'Loads our fixtures from accounts/management/commands/load_all_fixtures.py -> FIXTURES'

    def handle(self, *args, **kwargs):
    	for fixture in FIXTURES:
        	call_command('loaddata', fixture)
