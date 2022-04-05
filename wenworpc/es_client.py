#encoding=utf-8

import grpc
from wenworpc.wenworpc import elastic_pb2_grpc
from wenworpc.wenworpc import elastic_pb2
from django.conf import settings


class EsClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel("127.0.0.1:50250", options=options)
        self.stub = elastic_pb2_grpc.GlobalSearchStub(channel)

    def get_search(self, sync_way:str, page:int = 1, pagesize:int = 10, consumer_token: str = None):
        return self.stub.getSearch(
            elastic_pb2.GlobalSearchRequest(
                consumer_token=consumer_token,
                sync_wau=sync_way,
                page=page,
                pagesize=pagesize
            )
        )

