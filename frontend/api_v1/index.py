#encoding=utf-8

import pytz
import json
import logging
import markdown
from django.shortcuts import render
from common.helpers import (
    ok_json,
    error_json
)
from django.http import JsonResponse
from django.db.models import F
from wenwo.models import Banner
from django.core import serializers
from django.shortcuts import redirect
from django.conf import settings
from blog.form.article_forms import ArticleForm
from video_tutorial.models import Video
from blog.models import Article
from topic.models import Topic
from book.models import Course
from wenwo_auth.helper import check_api_token, check_user_token


@check_api_token
def get_index(request):
    course_tuijian_list = Course.objects.filter(is_active=True).order_by("-article_num")[0:3]
    ct_data = []
    vh_data = []
    hot_cdata = []
    for ct in course_tuijian_list:
        ct_data.append(ct.list_to_dict())
    video_hot_list = Video.objects.filter(is_active=True).order_by("-views")[0:8]
    for video_hot in video_hot_list:
        vh_data.append(video_hot.list_to_dict())
    course_hot_list = Course.objects.filter(is_active=True).order_by("-views")[0:30]
    for course_hot in course_hot_list:
        hot_cdata.append(course_hot.list_to_dict())
    ireturn_data = {
        "recommend_course":ct_data,
        "hot_video": vh_data,
        "hot_course": hot_cdata
    }
    return ok_json(ireturn_data)





