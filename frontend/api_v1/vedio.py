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
from video_tutorial.models import Video, Charpter, VideoReply, VideoCategory, UserBuyVideo
from wenwo_auth.helper import check_api_token, check_user_token


@check_api_token
def vedio_list(request):
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    video_return_data = []
    video_list = Video.objects.filter(is_active=True).order_by("-id")[start:end]
    for video in video_list:
        video_return_data.append(video.list_to_dict())
    return ok_json(video_return_data)


@check_api_token
def vedio_detail(request):
    params = json.loads(request.body.decode())
    vedio_id = int(params.get('vedio_id', 0))
    video = Video.objects.filter(id=vedio_id).first()
    return ok_json(video.detail_to_dict())


@check_api_token
@check_user_token
def create_vcmt(request):
    params = json.loads(request.body.decode())
    vedio_id = int(params.get('vedio_id', 0))
    chapter_id = int(params.get('chapter_id', 0))
    cmt_id = int(params.get('cmt_id', 0))
    user_id = int(params.get('user_id', 0))
    content = params.get('content', "")
    vedio = Video.objects.filter(id=vedio_id).first()
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("评论的用户不存在", 1000)
    if vedio is None:
        return error_json("评论的视频不存在", 1000)
    chapter = Charpter.objects.filter(id=chapter_id).first()
    if chapter is None:
        return error_json("评论的视频章节不存在", 1000)
    if content in ["", None]:
        return error_json("评论的内容不能为空", 1000)
    VideoReply.objects.create(
        video=vedio,
        reply_id=cmt_id,
        user=user,
        content=content
    )
    vedio.cmts = vedio.cmts + 1
    vedio.save()
    return ok_json("评论成功")


@check_api_token
def vcmt_list(request):
    params = json.loads(request.body.decode())
    vedio_id = int(params.get('vedio_id', 0))
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    video_reply_list = VideoReply.objects.filter(
        video__id=vedio_id,
        reply_id=0
    ).order_by("-id")[start:end]
    video_reply_return = []
    for video_reply in video_reply_list:
        video_reply_return.append(video_reply.to_dict())
    return ok_json(video_reply_return)


@check_api_token
@check_user_token
def vedio_like(request):
    params = json.loads(request.body.decode())
    vedio_id = int(params.get('vedio_id', 0))
    vedio = Video.objects.filter(id=vedio_id).first()
    vedio.like = vedio.like + 1 if vedio is not None else vedio.like
    vedio.save()
    return ok_json("视频点赞成功")