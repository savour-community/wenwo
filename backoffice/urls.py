from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from backoffice.views.blog import (
    back_blog_cat_list,
    back_blog_list,
    back_blog_check,
    back_blog_detail
)
from backoffice.views.user import (
    backend_login,
    backend_logout,
    back_user_list,
    back_user_detail,
    back_user_wallet,
    back_uw_record,
)
from backoffice.views.question import (
    back_topic_cat_list,
    back_question_list,
    back_question_check,
    back_question_detail
)

from backoffice.views.course import (
    back_course_cat_list,
    back_course_list,
    back_course_check,
    back_course_detail,
    bc_article_list,
    bc_article_check,
    bc_article_detail,
)
from backoffice.views.video import (
    back_video_cat_list,
    back_vedio_list,
    back_vedio_check,
    back_vedio_detail,
    back_vedio_chapter,
    bv_chapter_checked
)
from backoffice.views.suggestion import (
    back_suggestion_detail,
    back_suggestion_list,
    accpet_suggestion
)
from backoffice.views.notice import (
    back_notice_list,
    back_notice_detail
)



urlpatterns: List[Any] = [
    path(r'back_blog_cat_list', back_blog_cat_list, name='back_blog_cat_list'),
    path(r'back_blog_list', back_blog_list, name='back_blog_list'),
    path(r'<int:bid>/back_blog_detail', back_blog_detail, name='back_blog_detail'),
    path(r'<int:bid>/back_blog_check', back_blog_check, name='back_blog_check'),

    path(r'backend_login', backend_login, name='backend_login'),
    path(r'backend_logout', backend_logout, name='backend_logout'),
    path(r'back_user_list', back_user_list, name='back_user_list'),
    path(r'back_user_wallet', back_user_wallet, name='back_user_wallet'),
    path(r'<int:uid>/back_user_detail', back_user_detail, name='back_user_detail'),
    path(r'<int:uid>/back_uw_record', back_uw_record, name='back_uw_record'),

    path(r'back_topic_cat_list', back_topic_cat_list, name='back_topic_cat_list'),
    path(r'back_question_list', back_question_list, name='back_question_list'),
    path(r'<int:tid>/back_question_check', back_question_check, name='back_question_check'),
    path(r'<int:tid>/back_question_detail', back_question_detail, name='back_question_detail'),
    path(r'back_suggestion_list', back_suggestion_list, name='back_suggestion_list'),
    path(r'<int:id>/back_suggestion_detail', back_suggestion_detail, name='back_suggestion_detail'),
    path(r'<int:id>/accpet_suggestion', accpet_suggestion, name='accpet_suggestion'),

    path(r'back_course_cat_list', back_course_cat_list, name='back_course_cat_list'),
    path(r'back_course_list', back_course_list, name='back_course_list'),
    path(r'<int:cid>/back_course_check', back_course_check, name='back_course_check'),
    path(r'<int:cid>/back_course_detail', back_course_detail, name='back_course_detail'),
    path(r'<int:cid>/bc_article_list', bc_article_list, name='bc_article_list'),
    path(r'<int:cid>/bc_article_check', bc_article_check, name='bc_article_check'),
    path(r'<int:cid>/bc_article_detail', bc_article_detail, name='bc_article_detail'),

    path(r'back_video_cat_list', back_video_cat_list, name='back_video_cat_list'),
    path(r'back_vedio_list', back_vedio_list, name='back_vedio_list'),
    path(r'<int:vid>/back_vedio_check', back_vedio_check, name='back_vedio_check'),
    path(r'<int:vid>/back_vedio_detail', back_vedio_detail, name='back_vedio_detail'),
    path(r'<int:cid>/back_vedio_chapter', back_vedio_chapter, name='back_vedio_chapter'),
    path(r'<int:vid>/bv_chapter_checked', bv_chapter_checked, name='bv_chapter_checked'),

    path(r'back_notice_list', back_notice_list, name='back_notice_list'),
    path(r'<int:id>/back_notice_detail', back_notice_detail, name='back_notice_detail'),
]
