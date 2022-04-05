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
from wenwo_auth.models import User, UserInfo
from book.models import Course, CourseCat, CourseCommet, CourseArtcle
from wenwo_auth.helper import check_api_token, check_user_token


@check_api_token
def cource_list(request):
    params = json.loads(request.body.decode())
    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    course_return_data =[]
    course_list = Course.objects.filter(is_active=True).order_by("-id")[start:end]
    for course in course_list:
        course_return_data.append(course.list_to_dict())
    return ok_json(course_return_data)


@check_api_token
def cource_detail(request):
    params = json.loads(request.body.decode())
    course_id = int(params.get('course_id', 0))
    course_detail = Course.objects.filter(id=course_id).first()
    course_detail.views += 1
    course_detail.save()
    return ok_json(course_detail.detail_to_dict())


@check_api_token
def cource_article(request):
    params = json.loads(request.body.decode())
    article_id = int(params.get('article_id', 0))
    cac = CourseArtcle.objects.filter(id=article_id).first()
    cac.views += 1
    cac.save()
    return ok_json(cac.cac_dict())


@check_api_token
def create_ca_cmt(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    course_id = int(params.get('course_id', 0))
    article_id = int(params.get('article_id', 0))
    content = params.get('content', "")
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("系统中的该用户不存在", 1000)
    course = Course.objects.filter(id=course_id).first()
    if course is None:
        return error_json("系统数据库中没有这个课程", 1000)
    cac = CourseArtcle.objects.filter(id=article_id).first()
    if cac is None:
        return error_json("系统内部不存在该文章", 1000)
    CourseCommet.objects.create(
        course=course,
        user=user,
        artcle=cac,
        content=content,
    )
    return ok_json("评论成功")


@check_api_token
def cmt_list(request):
    params = json.loads(request.body.decode())
    course_id = int(params.get('course_id', 0))
    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    cmts_list = CourseCommet.objects.filter(
        course=Course.objects.filter(id=course_id).first()
    ).order_by("-id")[start:end]
    cmt_return_data = []
    for cmt in cmts_list:
        cmt_return_data.append(cmt.list_to_dict())
    return ok_json(cmt_return_data)
