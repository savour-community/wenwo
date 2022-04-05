#encoding=utf-8

import grpc
from wenworpc.wenworpc import scrapy_pb2_grpc
from wenworpc.wenworpc import scrapy_pb2
from django.conf import settings


class ScrapyClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel(settings.SCRAPY_GRPC_CHANNEL_URL, options=options)
        self.stub = scrapy_pb2_grpc.ScrapyStub(channel)

    def get_actcle(self, page: int, pagesize: int, consumer_token: str = None):
        return self.stub.getArticles(
            scrapy_pb2.ArticleScrapyRequest(
                consumer_token=consumer_token,
                page=page,
                pagesize=pagesize
            )
        )

