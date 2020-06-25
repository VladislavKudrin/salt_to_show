from django.core.management.base import BaseCommand
from django.core.management import call_command
import requests


class Command(BaseCommand):
    help = 'Sets webhook'

    def handle(self, *args, **kwargs):
    	requests.get('https://api.telegram.org/bot952860374:AAEtZPhGqcX3_Slu7K2nSpP3jc5B6aBWGsM/setWebhook?url=https://saltish.co/api/telegram/')
