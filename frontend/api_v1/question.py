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
from topic.models import TopicCategory, Topic, TopicReply
from wenwo_auth.helper import check_api_token, check_user_token



@check_api_token
def question_cat(request):
    tcat_list = TopicCategory.objects.all()
    tcat_return_data = []
    for tcat in tcat_list:
        tcat_return_data.append(tcat.to_dict())
    return ok_json(tcat_return_data)


@check_api_token
@check_user_token
def create_question(request):
    params = json.loads(request.body.decode())
    user_id = params.get('cat_id', 0)
    cat_id = params.get('cat_id', 0)
    title = params.get('title', "")
    content = params.get('content', "")
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("该用户不存在", 1000)
    category = TopicCategory.objects.filter(id=cat_id).first()
    if category is None:
        return error_json("系统内部没有这个分类", 1000)
    if title in ["", None] or content in ["", None]:
        return error_json("问题标题和内容不能为空", 1000)
    topic_a = Topic.objects.filter(title=title).first()
    if topic_a is not None:
        return error_json("系统内部已经存在相同的问题了", 1000)
    Topic.objects.create(
        title=title,
        category=category,
        content=content,
        user=user
    )
    return ok_json("发布问题成功")


@check_api_token
def question_list(request):
    params = json.loads(request.body.decode())
    cat_id = params.get('cat_id', 0)
    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    if cat_id not in ["0", 0]:
        tcat = TopicCategory.objects.filter(id=cat_id).first()
        qs_list = Topic.objects.filter(category=tcat).order_by("-id")[start:end]
    else:
        qs_list = Topic.objects.all().order_by("-id")[start:end]
    qs_return_data = []
    for qs in qs_list:
        qs_return_data.append(qs.list_to_dict())
    return ok_json(qs_return_data)


@check_api_token
def question_detail(request):
    params = json.loads(request.body.decode())
    qs_id = int(params.get('qs_id', 0))
    topic = Topic.objects.filter(id=qs_id).first()
    return ok_json(topic.detail_to_dict())


@check_api_token
def question_reply(request):
    params = json.loads(request.body.decode())
    qs_id = int(params.get('qs_id', 0))
    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    reply_list = TopicReply.objects.filter(topic__id=qs_id).order_by("-id")[start:end]
    comment_reply_list = []
    for reply in reply_list:
        comment_reply_list.append(reply.to_dict())
    return ok_json(comment_reply_list)


@check_api_token
def create_reply(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    qs_id = int(params.get('qs_id', 0))
    reply_id = int(params.get('reply_id', 0))
    content = params.get('content', "")
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("您还没登陆, 请前去登陆", 1000)
    topic = Topic.objects.filter(id=qs_id).first()
    if topic is None:
        return error_json("您要评论的问题不存在", 1000)
    if content in ["", None]:
        return error_json("评论的内容不能为空", 1000)
    TopicReply.objects.create(
        topic=topic,
        reply_id=reply_id,
        user=user,
        content=content
    )
    return ok_json("评论成功")


@check_api_token
def qs_comment_like(request):
    params = json.loads(request.body.decode())
    cmt_id = int(params.get('cmt_id', 0))
    tp = TopicReply.objects.filter(id=cmt_id).first()
    if tp is None:
        return error_json("您要点赞的评论不存在", 1000)
    else:
        tp.like += 1
        tp.save()
        return ok_json("点赞成功")

