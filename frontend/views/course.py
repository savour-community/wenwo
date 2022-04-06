#encoding=utf-8

import logging
import markdown
from django.shortcuts import render
from django.shortcuts import redirect
from book.models import (
    Course,
    CourseCat,
    CourseArtcle,
    CourseCommet
)
from common.helpers import paged_items
from book.forms.cmt_forms import CourseCommetForm
from book.forms.course_form import CourseForm
from book.forms.course_article_forms import CourseArtcleForm
from wenwo_auth.models import User
from django.views.decorators.csrf import csrf_exempt
from common.helpers import dec, d0
from frontend.helper import check_user_login
from wenwo_auth.models import User, UserInfo
from django.http import HttpResponseRedirect


def course_list(request):
    nav_cat = "course"
    cat_id = request.GET.get("cat_id", 0)
    course_cat_list = CourseCat.objects.filter(is_active=True)
    course_list = Course.objects.filter(is_active=True, status='CheckPass').order_by("-id")
    total_course = len(course_list)
    if cat_id not in [0, "0"]:
        course_list = course_list.filter(category__id=cat_id)
    course_list = paged_items(request, course_list)
    return render(request, 'v2_front/course/course_list.html', locals())


def course_detail(request, cid):
    nav_cat = "course"
    course_detail = Course.objects.filter(id=cid).first()
    course_detail.views += 1
    course_detail.save()
    course_detail.detail = markdown.markdown(
        course_detail.detail,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    user = User.objects.filter(id=course_detail.user.id).first()
    if user is not None:
        user_info = UserInfo.objects.filter(user_id=course_detail.user.id).first()
    course_chapter_list = CourseArtcle.objects.filter(course=course_detail, status='CheckPass').order_by("id")
    return render(request, 'v2_front/course/course_detail.html', locals())


def course_article(request, cid):
    nav_cat = "course"
    act_id = int(request.GET.get("act_id", 0))
    user_id = request.session.get("user_id")
    is_comment = request.GET.get("is_comment", "No")
    course_detail = Course.objects.filter(id=cid).first()
    course_chapter_list = CourseArtcle.objects.filter(course=course_detail, status='CheckPass').order_by("part", "id")
    cs_comment_list = CourseCommet.objects.filter(course=course_detail, artcle__id=act_id).order_by("-id")
    total_cmt = len(cs_comment_list)
    if act_id != 0:
        course_chapter = CourseArtcle.objects.filter(id=act_id, status='CheckPass').first()
        course_chapter.views += 1
        course_chapter.save()
    else:
        course_chapter = CourseArtcle.objects.filter(course=course_detail, status='CheckPass').first()
        course_chapter.views += 1
        course_chapter.save()
    if course_chapter is not None:
        course_chapter.detail = markdown.markdown(
            course_chapter.detail,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
    if request.method == 'GET':
        cmt_form = CourseCommetForm(request)
        return render(request, 'v2_front/course/course_article.html', locals())
    if request.method == 'POST':
        is_login = request.session.get("is_login")
        if is_login:
            cmt_form = CourseCommetForm(request, request.POST)
            if cmt_form.is_valid():
                user = User.objects.filter(id=user_id).first()
                cmt_form.create_comment(course_detail, course_chapter, user)
                return HttpResponseRedirect(
                    "/" + str(cid) + '/course_article?act_id=' + str(act_id) + "&is_comment=Yes"
                )
            else:
                error = cmt_form.errors
                return render(
                    request,
                    "v2_front/course/course_article.html",
                    {
                        'cmt_form': cmt_form,
                        'error': error,
                        'course_detail': course_detail,
                        'course_chapter_list': course_chapter_list,
                        'cs_comment_list': cs_comment_list,
                        'total_cmt': len(total_cmt)
                    }
                )
        else:
            return redirect("register")


def course_article_like(request, aid):
    course_chapter = CourseArtcle.objects.filter(id=aid, status='CheckPass').first()
    course_chapter.like += 1
    course_chapter.save()
    return HttpResponseRedirect(
        "/" + str(course_chapter.course.id) + '/course_article?act_id=' + str(aid) + "&is_comment=Yes"
    )


@csrf_exempt
@check_user_login
def create_course(request):
    nav_cat = "course"
    tab_active = "my_course"
    user_id = request.session.get("user_id")
    if request.method == "GET":
        course_form = CourseForm(request)
        return render(request, "v2_front/auth/course/create_course.html", locals())
    if request.method == "POST":
        course_form = CourseForm(request, request.POST, request.FILES)
        if course_form.is_valid():
            user = User.objects.filter(id=user_id).first()
            course_form.create_course(user)
            return redirect('my_course')
        else:
            error = course_form.errors
            return render(
                request, "v2_front/auth/course/create_course.html",
                {
                    'user_id': int(uid),
                    'course_form': course_form,
                    'error': error
                }
            )


@csrf_exempt
@check_user_login
def update_course(request, cid):
    nav_cat = "course"
    tab_active = "my_course"
    course = Course.objects.filter(id=cid).first()
    uid = request.session.get("user_id")
    if request.method == "GET":
        course_form = CourseForm(request, instance=course)
        return render(request, "v2_front/auth/course/update_course.html", locals())
    if request.method == "POST":
        course_form = CourseForm(request, request.POST, request.FILES, instance=course)
        if course_form.is_valid():
            uid = course_form.update_course(cid)
            return redirect('my_course')
        else:
            error = course_form.errors
            return render(
                request, "v2_front/auth/course/update_course.html",
                {
                    "user_id": uid,
                    "course": course,
                    'course_form': course_form,
                    'error': error
                }
            )


@csrf_exempt
@check_user_login
def create_course_article(request, cid):
    nav_cat = "course"
    tab_active = "my_course"
    course_id = int(cid)
    c_article_list = CourseArtcle.objects.filter(course__id=cid)
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if request.method == "GET":
        course_article_form = CourseArtcleForm(request)
        return render(request, "v2_front/auth/course/add_course_time.html", locals())
    if request.method == "POST":
        course_article_form = CourseArtcleForm(request, request.POST)
        if course_article_form.is_valid():
            course_article_form.create_article(int(cid))
            return redirect('create_course_article', int(cid))
        else:
            error = course_article_form.errors
            return render(
                request, "v2_front/auth/course/add_course_time.html",
                {
                    "c_article_list": c_article_list,
                    "user": user,
                    "course_id": course_id,
                    'user_id': user_id,
                    'course_article_form': course_article_form,
                    'error': error
                }
            )


@csrf_exempt
@check_user_login
def wirte_course_article(request, act_id):
    nav_cat = "course"
    tab_active = "my_course"
    c_article = CourseArtcle.objects.filter(id=act_id).first()
    c_article_id = act_id
    uid = request.session.get("user_id")
    if request.method == "GET":
        course_article_form = CourseArtcleForm(request, instance=c_article)
        return render(request, "v2_front/auth/course/wirte_course_arctle.html", locals())
    if request.method == "POST":
        course_article_form = CourseArtcleForm(request, request.POST, instance=c_article)
        if course_article_form.is_valid():
            uid = course_article_form.update_article(act_id)
            return redirect('create_course_article', int(c_article.course.id))
        else:
            error = course_article_form.errors
            return render(
                request, "v2_front/auth/course/wirte_course_arctle.html",
                {
                    "user_id": uid,
                    "c_article": c_article,
                    'course_article_form': course_article_form,
                    'error': error
                }
            )
