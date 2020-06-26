from django.core.management.base import BaseCommand
from django.core.management import call_command
import requests
from django.conf import settings


class Command(BaseCommand):
    help = 'Set webhook for local'

    def handle(self, *args, **kwargs):
    	if not settings.LIVE:
    		t = requests.get('https://api.telegram.org/bot1261478236:AAGtaxf4gqGf562PIcCXmkK7cHGjVQKNf5M/setWebhook?url='+settings.BASE_URL+'/api/telegram/')
    		print(t.text)
