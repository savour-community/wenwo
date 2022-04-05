#encoding=utf-8


import logging
from django.core.management.base import BaseCommand
from wenworpc.es_client import EsClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        es_client = EsClient()
        ret_info = es_client.get_search('Video')
        print("ret_info====", ret_info)