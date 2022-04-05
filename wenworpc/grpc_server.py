#encoding=utf-8

import logging
import json
import pytz
from blog.models import Article
from book.models import Course
from video_tutorial.models import Video
from topic.models import Topic
from activity.models import Activity
from wenworpc.wenworpc import elastic_pb2_grpc
from wenworpc.wenworpc import elastic_pb2
from wenworpc.wenworpc import common_pb2
from wenwo_auth.models import UserInfo
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


class EsServer(elastic_pb2_grpc.GlobalSearchServicer):
    def getSearch(self, request, context):
        sync_way = request.sync_wau
        page = request.page - 1
        pagesize = request.pagesize
        start = page * pagesize
        end = start + pagesize
        if sync_way in ['blog', 'Blog', 'BLOG']:
            blog_list = Article.objects.filter(is_check='Yes').order_by("-id")[start:end]
            blog_return_list = []
            for blog in blog_list:
                try:
                    user_info = UserInfo.objects.filter(user_id=blog.user.id).first()
                    author_photo = str(user_info.user_pho)
                except:
                    author_photo = ""
                item = elastic_pb2.GlobalSearchContent(
                    title=blog.title,
                    author=blog.user.user_name,
                    author_photo=author_photo,
                    img="",
                    views=blog.views,
                    like=blog.like,
                    answer=blog.cmts,
                    content=blog.excerpt,
                    price="0.00",
                    created=blog.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M')
                )
                blog_return_list.append(item)
            return elastic_pb2.GlobalSearchResponse(
                gs_content=blog_return_list
            )
        elif sync_way in ['book', 'Book', 'BOOK']:
            book_list = Course.objects.filter(status='Checked').order_by("-id")[start:end]
            book_return_list = []
            for book in book_list:
                try:
                    user_info = UserInfo.objects.filter(user_id=book.user.id).first()
                    author_photo = str(user_info.user_pho)
                except:
                    author_photo = ""
                item = elastic_pb2.GlobalSearchContent(
                    title=book.title,
                    author=book.user.user_name,
                    author_photo=author_photo,
                    img=str(book.logo),
                    views=book.views,
                    like=book.buyer_num,
                    answer=book.article_num,
                    content=book.excerpt,
                    price=str(book.price),
                    created=book.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M')
                )
                book_return_list.append(item)
            return elastic_pb2.GlobalSearchResponse(
                gs_content=book_return_list
            )
        elif sync_way in ['video', 'Video', 'VIDEO']:
            video_list = Video.objects.filter(status='CheckPass').order_by("-id")[start:end]
            video_return_list = []
            for video in video_list:
                try:
                    user_info = UserInfo.objects.filter(user_id=video.user.id).first()
                    author_photo = str(user_info.user_pho)
                except:
                    author_photo = ""
                item = elastic_pb2.GlobalSearchContent(
                    title=video.title,
                    author=video.user.user_name,
                    author_photo=author_photo,
                    img=str(video.video_img),
                    views=video.views,
                    like=video.like,
                    answer=video.cmts,
                    content=video.excerpt,
                    price=str(video.price),
                    created=video.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M')
                )
                print("item ===", item)
                video_return_list.append(item)
            return elastic_pb2.GlobalSearchResponse(
                gs_content=video_return_list
            )
        elif sync_way in ['question', 'Question', 'QUESTION']:
            question_list = Topic.objects.filter(is_check='Yes').order_by("-id")[start:end]
            questio_return_list = []
            for questio in question_list:
                try:
                    user_info = UserInfo.objects.filter(user_id=questio.user.id).first()
                    author_photo = str(user_info.user_pho)
                except:
                    author_photo = ""
                item = elastic_pb2.GlobalSearchContent(
                    title=questio.title,
                    author=questio.user.user_name,
                    author_photo=author_photo,
                    img="",
                    views=questio.views,
                    like=questio.like,
                    answer=questio.answers,
                    content=questio.excerpt,
                    price="0.00",
                    created=questio.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M')
                )
                questio_return_list.append(item)
            return elastic_pb2.GlobalSearchResponse(
                gs_content=questio_return_list
            )
        else:
            activity_list = Activity.objects.filter(is_active=True).order_by("-id")[start:end]
            activity_return_list = []
            for activity in activity_list:
                try:
                    user_info = UserInfo.objects.filter(user_id=activity.user.id).first()
                    author_photo = str(user_info.user_pho)
                except:
                    author_photo = ""
                item = elastic_pb2.GlobalSearchContent(
                    title=activity.title,
                    author=activity.user.user_name,
                    author_photo=author_photo,
                    img=str(activity.img),
                    views=activity.views,
                    like=0,
                    answer=0,
                    content=activity.excerpt,
                    price=str(activity.price),
                    created=activity.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M')
                )
                activity_return_list.append(item)
            return elastic_pb2.GlobalSearchResponse(
                gs_content=activity_return_list
            )
