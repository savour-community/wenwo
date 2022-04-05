#encoding=utf-8

import pytz
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
    paged_items,
    ok_json,
    error_json
)
from django.http import JsonResponse
from django.db.models import F
from wenwo.models import Banner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.shortcuts import redirect
from django.conf import settings
from blog.form.cmt_forms import BlogReplyForm
from blog.form.article_forms import ArticleForm
from wenwo_auth.models import User, UserInfo
from frontend.helper import check_user_login


tz = pytz.timezone(settings.TIME_ZONE)


def index(request):
    nav_cat = "index"
    cat_id = int(request.GET.get("cat_id", 0))
    title = request.GET.get("title", "")
    cat_name_lists = Category.objects.all()
    if cat_id not in ["0", 0]:
        category = Category.objects.filter(id=cat_id).first()
        blog_list = Article.objects.filter(
            category=category, is_check='Yes'
        ).order_by("-id")[0:30]
    else:
        blog_list = Article.objects.filter(is_check='Yes').order_by("-id")[0:30]
    if title not in ["", None]:
        blog_list = Article.objects.filter(title__icontains=title).order_by("-id")
    for blog in blog_list:
        user_info = UserInfo.objects.filter(user_id=blog.user.id).first()
        if user_info is not None:
            blog.user.user_pho = user_info.user_pho
    user_order_list = User.objects.all().order_by("-login_times")[0:20]
    for user_order in user_order_list:
        user_info = UserInfo.objects.filter(user_id=user_order.id).first()
        if user_info is not None:
            user_order.user_pho = user_info.user_pho
            user_order.user_pos = user_info.user_pos
    return render(request, 'v2_front/blog/blog_list.html', locals())


def article_list(request):
    cat_id = request.GET.get('cat_id', 0)
    page = int(request.GET.get('page', 20))
    page_size = int(request.GET.get('page_size', 1))
    start = page * page_size
    end = start + page_size
    if cat_id in ["0", 0]:
        article_lst = Article.objects.filter(
            is_active=True,
            is_check='Yes'
        ).order_by('-id')[start:end]
    else:
        cat = Category.objects.filter(id=cat_id).order_by("-id").first()
        article_lst = Article.objects.filter(
            category=cat,
            is_check='Yes'
        ).order_by('-id')[start:end]
    article_list = []
    total = len(article_lst)
    for article in article_lst:
        created_at = article.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
        user_info = UserInfo.objects.filter(user_id=article.user.id).first()
        user_pho = user_info.user_pho if user_info is not None else ""
        a_t_l = {
            "id": article.id,
            "title": article.title,
            "excerpt": article.excerpt,
            "img": str(article.img),
            'user': article.user.user_name,
            'user_pho': str(user_pho),
            "cmts": article.cmts,
            "like": article.like,
            'views': article.views,
            'created_at': created_at,
        }
        article_list.append(a_t_l)
    ret_data = {
        "total": total,
        "data": article_list
    }
    return ok_json(ret_data)


def blog_detail(request, sid):
    nav_cat = "index"
    user_id = request.session.get("user_id")
    is_comment = request.GET.get("is_comment", "No")
    show = Article.objects.get(id=sid)
    hot_list = Article.objects.all().order_by('-views')[:30]
    tag_name_lists = Tag.objects.all().order_by('-id')
    blog_comment_list = BlogReply.objects.filter(arcticle=show).order_by('-id')
    blog_reply_num = len(blog_comment_list)
    show.views = show.views + 1
    show.save()
    show.body = markdown.markdown(
        show.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    if request.method == 'GET':
        cmt_form = BlogReplyForm(request)
        return render(request, 'v2_front/blog/blog_detail.html', locals())
    if request.method == 'POST':
        is_login = request.session.get("is_login")
        if is_login:
            cmt_form = BlogReplyForm(request, request.POST)
            if cmt_form.is_valid():
                user = User.objects.filter(id=user_id).first()
                cmt_show = Article.objects.get(id=sid)
                cmt_form.create_comment(cmt_show, 0, user)
                cmt_show.cmts += 1
                cmt_show.save()
                return redirect("blog_detail", sid)
            else:
                error = cmt_form.errors
                return render(
                    request,
                    "v2_front/blog/blog_detail.html",
                    {
                        'cmt_form': cmt_form,
                        'error': error,
                        'show': show,
                        'hot_list': hot_list,
                        'tag_name_lists': tag_name_lists,
                        'blog_comment_list': blog_comment_list,
                        'blog_reply_num': len(blog_comment_list),
                        'is_comment': is_comment
                    }
                )
        else:
            return redirect("register")


@check_user_login
def blog_like(request, id):
    article = Article.objects.get(id=id)
    article.like += 1
    article.save()
    return redirect("blog_detail", id)


@check_user_login
def write_blog(request):
    tab_active = "blog"
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if request.method == 'GET':
        act_form = ArticleForm(request)
        return render(request, 'v2_front/auth/blog/write_blog.html', locals())
    if request.method == 'POST':
        act_form = ArticleForm(request, request.POST)
        if act_form.is_valid():
            act_form.create_blog(user)
            return redirect('index')
        else:
            error = act_form.errors
            return render(
                request, "v2_front/auth/blog/write_blog.html",
                {
                    'act_form': act_form,
                    'error': error
                }
            )


@check_user_login
def update_blog(request, bid):
    blog = Article.objects.filter(id=bid).first()
    if blog.is_check == "Yes":
        return redirect("blog_detail", bid)
    if request.method == 'GET':
        act_form = ArticleForm(request, instance=blog)
        return render(request, 'v2_front/auth/blog/update_blog.html', locals())
    if request.method == 'POST':
        act_form = ArticleForm(request, request.POST, instance=blog)
        if act_form.is_valid():
            act_form.upate_blog(bid)
            return redirect('index')
        else:
            error = act_form.errors
            return render(
                request, "v2_front/auth/blog/update_blog.html",
                {
                    'act_form': act_form,
                    'error': error,
                    'blog': blog
                }
            )

