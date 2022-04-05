#encoding=utf-8

import logging
from django.shortcuts import render
from video_tutorial.models import (
    Video,
    VideoCategory,
    Charpter,
    VideoReply)
from common.helpers import paged_items, ok_json, error_json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import JsonResponse
from django.db.models import F


def video_list(request):
    lid = request.GET.get('lid')
    page = request.GET.get('page')
    logging.info("cat lid is %s and page is %s", lid, page)
    video_lists = Video.objects.all()
    video_cat_list = VideoCategory.objects.all()
    hot_list = Video.objects.all().order_by('-views')[0:15]
    total_class = len(video_lists)
    if lid not in [0, '0', '', None]:
        video_lists = video_lists.filter(category__id=lid)
    video_lists = video_lists.order_by('-id')
    paginator = Paginator(video_lists, 50)
    try:
        video_list = paginator.page(page)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)
    if request.is_ajax():
        json_data = serializers.serialize("json", video_list, ensure_ascii=False)
        return ok_json({'video_list': json_data})
    return render(request, 'frontend/video_tutorial/back_vedio_list.html', locals())


def video_detail(request, video_id):
    logging.info("request id is %s", video_id)
    video = Video.objects.get(id=video_id)
    chapter_list = Charpter.objects.filter(video_id=video_id)
    # content_list = Contents.objects.filter(video_id=video_id)
    video_reply_list = VideoReply.objects.filter(video_id=video_id).order_by('-id')
    video_reply_num = len(video_reply_list)
    video.views = video.views + 1
    video.save()
    return render(request, 'frontend/video_tutorial/video_detail.html', locals())


def set_video_commet(request):
    logging.info("enter .....")
    video_id = request.POST.get('video_id')
    reply_id = request.POST.get('reply_id')
    account_id = request.POST.get('user_id')
    content = request.POST.get('content')
    if account_id in [0, '', None]:
        return error_json("用户没有登陆，请登陆")
    logging.info("video_id: %s, reply_id: %s, account_id: %s, content: %s",
                 video_id, reply_id, account_id, content)
    if content in ['', None]:
        return error_json("评论的内容不能为空")
    else:
        try:
            VideoReply.objects.create(
                video_id=video_id,
                reply_id=reply_id,
                account_id=account_id,
                content=content,
            )
            return ok_json("评论成功")
        except:
            return error_json("评论失败, 请检查是否已经登陆")


def video_like(request):
    video_id = request.GET.get("id")
    logging.info("video_id id is %s", video_id)
    Video.objects.filter(id=video_id).update(like=F('like') + 1)
    video_model = Video.objects.filter(id=video_id).values('like')
    total_like = video_model[0]['like']
    return JsonResponse({'total_like': total_like})


def vedio_reply_like(request):
    reply_id = request.GET.get("id")
    logging.info("topic id is %s", reply_id)
    VideoReply.objects.filter(id=reply_id).update(like=F('like') + 1)
    video_reply = VideoReply.objects.filter(id=reply_id).values('like')
    video_reply_like = video_reply[0]['like']
    return JsonResponse({'video_reply_like': video_reply_like})










