#encoding=utf-8

import pytz
import json
import logging
import markdown
from django.shortcuts import render
from blog.models import (
    Category,
    Article,
    Tag,
    BlogReply
)
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
from wenwo_auth.helper import check_api_token, check_user_token


@check_api_token
def blog_cat(request):
    blog_cat_list = Category.objects.filter(is_active=True)
    category_return_data = []
    for blog_cat in blog_cat_list:
        category_return_data.append(blog_cat.to_dict())
    return ok_json(category_return_data)


@check_api_token
def blog_list(request):
    params = json.loads(request.body.decode())
    cat_id = params.get('cat_id', 0)
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    if cat_id not in [0, "0"]:
        category = Category.objects.filter(id=cat_id).first()
        arcicle_list = Article.objects.filter(
            category=category,
            is_active=True,
            is_check='Yes',
        ).order_by("-id")[start:end]
    else:
        arcicle_list = Article.objects.filter(
            is_active=True,
            is_check='Yes',
        ).order_by("-id")[start:end]
    blog_data_return = []
    for arcicle in arcicle_list:
        blog_data_return.append(arcicle.list_to_dict())
    return ok_json(blog_data_return)


@check_api_token
def blog_detail(request):
    params = json.loads(request.body.decode())
    blog_id = int(params.get('blog_id', 0))
    artcile = Article.objects.filter(id=blog_id).first()
    return ok_json(artcile.detail_to_dict())


@check_api_token
def comment_list(request):
    params = json.loads(request.body.decode())
    blog_id = int(params.get('blog_id', 0))
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = page * page_size
    end = start + page_size
    artcile = Article.objects.filter(id=blog_id).first()
    br_list = BlogReply.objects.filter(arcticle=artcile, reply_id=0).order_by("-id")[start:end]
    br_return_data = []
    for br in br_list:
        br_return_data.append(br.to_dict())
    return ok_json(br_return_data)


@check_api_token
def blog_like(request):
    params = json.loads(request.body.decode())
    blog_id = int(params.get('blog_id', 0))
    artcile = Article.objects.filter(id=blog_id).first()
    artcile.like = artcile.like + 1 if artcile is not None else artcile.like
    artcile.save()
    return ok_json("博客点赞成功")


@check_api_token
def create_cmt_reply(request):
    params = json.loads(request.body.decode())
    blog_id = int(params.get('blog_id', 0))
    cmt_id = int(params.get('cmt_id', 0))
    user_id = int(params.get('user_id', 0))
    content = params.get('content', "")
    artcile = Article.objects.filter(id=blog_id).first()
    if artcile is None:
        return error_json("评论的博客不存在", 1000)
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("评论的用户不存在", 1000)
    if content in ["", None]:
        return error_json("评论的内容不能为空", 1000)
    BlogReply.objects.create(
        arcticle=artcile,
        reply_id=cmt_id,
        user=user,
        content=content,
    )
    artcile.cmts = artcile.cmts + 1
    artcile.save()
    return ok_json("评论成功")


@check_api_token
def cmt_reply_like(request):
    params = json.loads(request.body.decode())
    cmt_reply_id = int(params.get('cmt_reply_id', 0))
    br = BlogReply.objects.filter(id=cmt_reply_id).first()
    br.like = br.like + 1 if br is not None else br.like
    br.save()
    return ok_json("评论点赞成功")