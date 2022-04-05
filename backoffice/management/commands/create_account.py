# encoding=utf-8

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from wenwo_auth.helper import hash_code
from wenwo_auth.models import Account


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'user_name',
            type=str,
            help='Please input user name'
        )

        parser.add_argument(
            'password',
            type=str,
            help='Please input password'
        )

        parser.add_argument(
            '--type',
            type=str,
            default='Admin',
            help='Please input type Admin | Outer | Inner ')

    def handle(self, *args, **options):
        user_name = options['user_name']
        password = options['password']
        type = options['type']
        Account.objects.update_or_create(
            name=user_name,
            defaults={
                "password": hash_code(password),
                "role": type,
            }
        )
        print("create ", user_name, password, type, "success")

