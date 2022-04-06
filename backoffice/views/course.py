#encoding=utf-8

import markdown
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from book.models import Course, CourseCat, CourseArtcle
from backoffice.helper import check_admin_login


@check_admin_login
def back_course_cat_list(request):
    b_cat_list = CourseCat.objects.all().order_by("-id")
    return render(request, 'backend/blog/blog_cat_list.html', locals())


@check_admin_login
def back_course_list(request):
    title = request.GET.get("title", "")
    b_course_list = Course.objects.all().order_by("-id")
    if title not in ["", None]:
        b_course_list = b_course_list.filter(title__icontains=title)
    back_cs_list = paged_items(request, b_course_list)
    return render(request, 'backend/course/course_list.html', locals())


@check_admin_login
def back_course_check(request, cid):
    status = request.GET.get("status", "CheckPass")
    b_course_detail = Course.objects.filter(id=cid).first()
    b_course_detail.status = status
    if status == "CheckFail":
        b_course_detail.check_reason =\
            "请检查文章格式是否正确，内容是否包含广告和内容是否触犯国家法律法规"
    b_course_detail.is_active = True
    b_course_detail.save()
    return redirect('back_course_list')


@check_admin_login
def back_course_detail(request, cid):
    b_course_detail = Course.objects.filter(id=cid).first()
    b_course_detail.detail = markdown.markdown(
        b_course_detail.detail,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    return render(request, 'backend/course/course_detail.html', locals())


@check_admin_login
def bc_article_list(request, cid):
    b_article_list = CourseArtcle.objects.filter(course__id=cid).order_by('id')
    b_article_list = paged_items(request, b_article_list)
    return render(request, 'backend/course/course_article.html', locals())


@check_admin_login
def bc_article_check(request, cid):
    status = request.GET.get("status", "CheckPass")
    b_course_article = CourseArtcle.objects.filter(id=cid).first()
    b_course_article.status = status
    if status == "CheckFail":
        b_course_article.check_reason = \
            "请检查文章格式是否正确，内容是否包含广告和内容是否触犯国家法律法规"
    b_course_article.is_active = True
    b_course_article.save()
    return redirect('bc_article_list', b_course_article.course.id)


@check_admin_login
def bc_article_detail(request, cid):
    bc_article = CourseArtcle.objects.filter(course__id=cid).first()
    if bc_article is not None:
        bc_article.detail = markdown.markdown(
            bc_article.detail,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
    return render(request, 'backend/course/course_article_detail.html', locals())


