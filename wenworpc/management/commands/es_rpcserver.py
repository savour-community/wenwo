#encoding=utf-8

import grpc
from django.core.management.base import BaseCommand
from concurrent import futures
from wenworpc.wenworpc import elastic_pb2_grpc
from wenworpc.grpc_server import EsServer


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        elastic_pb2_grpc.add_GlobalSearchServicer_to_server(
            EsServer(),
            server
        )
        server.add_insecure_port('[::]:50250')
        server.start()
        server.wait_for_termination()