#encoding=utf-8

import logging
from django.core.management.base import BaseCommand
from common.helpers import sleep
from about.test import add_list, return_list


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=float,
            default=1,
            help='sleep interval in min'
        )

    def handle(self, *args, **options):
        while True:
            logging.info("options = %s", options['interval'])
            add_list(options['interval'])
            print(return_list())
            sleep(options['interval'])
