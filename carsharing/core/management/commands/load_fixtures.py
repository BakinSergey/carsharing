import json
import sys, os
import subprocess

from collections import defaultdict
from django.conf import settings

from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--model',
            dest='model',
            default=None,
            type=str,
            help='make Fixture only specified model',
        )

    def handle(self, **options):
        FIX_DIR = settings.FIXTURE_DIRS
        fixtures = []
        if options['model']:
            fix_filename = options['model'] + '.json'
            if os.path.exists(os.path.join(FIX_DIR[0], fix_filename)):
                fixtures.append(fix_filename)
            else:
                print(f'fixtures for model {options["model"]} not found')
        else:
            fixtures = os.listdir(FIX_DIR[0])

        if fixtures:
            for fixture in fixtures:
                args = ["python", "manage.py", "loaddata", fixture]
                try:
                    process = subprocess.Popen(args, stdout=subprocess.PIPE)
                    data = process.communicate()
                except:
                    return
                if data[0]:
                    self.stdout.write(self.style.SUCCESS('fixture {} applied:'.format(fixture)))
                    self.stdout.write(self.style.SUCCESS(data[0].decode('utf-8')))
                else:
                    self.stdout.write(self.style.ERROR('wrong fixture file: {}'.format(fixture)))









