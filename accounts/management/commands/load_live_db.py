from django.core.management.base import BaseCommand

from ecommerce.backup_utils import (
    backup_and_download_live_db, 
    load_in_local_backup_db
)


class Command(BaseCommand):
    help = 'Grab life data from heroku'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ignore-download',
            action='store_true',
            dest='ignore-download',
        )
        parser.add_argument(
            '--ignore-load-in',
            action='store_true',
            dest='ignore-load-in',
        )

    def handle(self, *args, **options):
        print("Backing up live db.")
        if not options.get('ignore-download'):
            backup_and_download_live_db()
        if not options.get('ignore-load-in'):
            load_in_local_backup_db()