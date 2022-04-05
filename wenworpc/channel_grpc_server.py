#encoding=utf-8

import logging
import json
import pytz
from blog.models import Article
from book.models import Course
from wenworpc.wenworpc import channel_pb2
from wenworpc.wenworpc import channel_pb2_grpc
from wenworpc.wenworpc import common_pb2
from django.conf import settings


tz = pytz.timezone(settings.TIME_ZONE)


def grpc_error(error_msg='', response=None):
    error = common_pb2.Error(
        code=1,
        brief=error_msg,
        detail=error_msg,
        can_retry=True)
    if response:
        return response(error=error)
    return error


class ChannelPtmServer(channel_pb2_grpc.ChannelPtmServicer):
    def getChannel(self, request, context):
        sync_way = request.sync_way
        page = request.page - 1
        pagesize = request.pagesize
        start = page * pagesize
        end = start + pagesize
        blog_list = Article.objects.filter(is_check='Yes', is_sync=False).order_by("-id")[start:end]
        blog_return_list = []
        for blog in blog_list:
            item = channel_pb2.ChannelPlatform(
                title=blog.title,
                abstruct=blog.excerpt,
                content=blog.body
            )
            blog_return_list.append(item)
        return channel_pb2.ChannelPtResponse(
            cpt=blog_return_list
        )