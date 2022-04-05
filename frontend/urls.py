from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from frontend.views.blog import (
    index,
    article_list,
    blog_detail,
    write_blog,
    update_blog,
    blog_like
)
from frontend.views.video import (
    video_list,
    video_detail,
    video_chapter,
    create_video,
    update_video,
    create_video_chapter
)

from frontend.views.course import (
    course_list,
    course_detail,
    course_article,
    create_course,
    update_course,
    wirte_course_article,
    create_course_article,
    course_article_like
)
from frontend.views.question import (
    create_question,
    question_list,
    question_detail
)

from frontend.views.activity import (
    activity_list,
    activity_detail
)

from frontend.views.auth import (
    sms_send,
    sms_check,
    login,
    register,
    forget,
    logout,
    person_info,
    update_user_info,
    my_blog,
    my_question,
    my_wallet,
    withdraw_wallet,
    my_course,
    my_video,
    my_focus_web,
    focus_me_web,
    focus_other_web
)
from frontend.views.suggestion import my_suggestion, create_sgt
from frontend.views.author import (
    author_order,
    author_main,
    his_blog,
    his_video,
    his_course
)
from frontend.views.about import download


urlpatterns: List[Any] = [
    # 博客
    path(r'', index, name='index'),
    path(r'write_blog', write_blog, name='write_blog'),
    path(r'<int:bid>/update_blog', update_blog, name='update_blog'),
    path(r'<int:id>/blog_like', blog_like, name='blog_like'),
    path(r'article_list', article_list, name='article_list'),
    path(r'blog_detail-<int:sid>.html', blog_detail, name='blog_detail'),

    # 专栏课程
    path(r'course_list', course_list, name='course_list'),
    path(r'<int:cid>/course_detail', course_detail, name='course_detail'),
    path(r'<int:cid>/course_article', course_article, name='course_article'),
    path(r'create_course', create_course, name='create_course'),
    path(r'<int:cid>/update_course', update_course, name='update_course'),
    path(r'<int:cid>/create_course_article', create_course_article, name='create_course_article'),
    path(r'<int:act_id>/wirte_course_article', wirte_course_article, name='wirte_course_article'),
    path(r'<int:aid>/course_article_like', course_article_like, name='course_article_like'),


    # 视频教程
    path(r'video_list', video_list, name='video_list'),
    path(r'<int:vid>/video_detail', video_detail, name='video_detail'),
    path(r'<int:vid>/video_chapter', video_chapter, name='video_chapter'),
    path(r'create_video', create_video, name='create_video'),
    path(r'<int:vid>/update_video', update_video, name='update_video'),
    path(r'<int:vid>/create_video_chapter', create_video_chapter, name='create_video_chapter'),

    # 问题
    path(r'question_list', question_list, name='question_list'),
    path(r'create_question', create_question, name='create_question'),
    path(r'question_detail-<int:qid>.html', question_detail, name='question_detail'),
    path(r'activity_list', activity_list, name='activity_list'),
    path(r'activity_detail-<int:sid>.html', activity_detail, name='activity_detail'),

    # 用户权限
    path(r'sms_send', sms_send, name='sms_send'),
    path(r'sms_check', sms_check, name='sms_check'),
    path(r'login', login, name='login'),
    path(r'register', register, name='register'),
    path(r'forget', forget, name='forget'),
    path(r'logout', logout, name='logout'),
    path(r'person_info', person_info, name='person_info'),
    path(r'<int:uid>/update_user_info', update_user_info, name='update_user_info'),
    path(r'my_blog', my_blog, name='my_blog'),
    path(r'my_question', my_question, name='my_question'),
    path(r'my_wallet', my_wallet, name='my_wallet'),
    path(r'withdraw_wallet', withdraw_wallet, name='withdraw_wallet'),
    path(r'my_course', my_course, name='my_course'),
    path(r'my_suggestion', my_suggestion, name='my_suggestion'),
    path(r'create_sgt', create_sgt, name='create_sgt'),
    path(r'my_video', my_video, name='my_video'),
    path(r'my_focus_web', my_focus_web, name='my_focus_web'),
    path(r'focus_me_web', focus_me_web, name='focus_me_web'),
    path(r'<int:fid>/focus_other_web', focus_other_web, name='focus_other_web'),

    # 作者相关页面
    path(r'author_order', author_order, name='author_order'),
    path(r'<int:uid>/author_main', author_main, name='author_main'),
    path(r'<int:uid>/his_blog', his_blog, name='his_blog'),
    path(r'<int:uid>/his_video', his_video, name='his_video'),
    path(r'<int:uid>/his_course', his_course, name='his_course'),

    path(r'download', download, name='download'),
]

