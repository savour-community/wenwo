from typing import Any, List
from django.contrib import admin
from django.urls import include, path
from frontend.api_v1.login import (
    sms_send,
    sms_check,
    login,
    register,
    forget,
    logout
)
from frontend.api_v1.blog import (
    blog_cat,
    blog_list,
    blog_detail,
    comment_list,
    blog_like,
    create_cmt_reply,
    cmt_reply_like
)
from frontend.api_v1.question import (
    question_cat,
    create_question,
    question_list,
    question_detail,
    question_reply,
    create_reply,
    qs_comment_like
)
from frontend.api_v1.course import (
    cource_list,
    cource_detail,
    cource_article,
    create_ca_cmt,
    cmt_list,
)
from frontend.api_v1.vedio import (
    vedio_list,
    vedio_detail,
    create_vcmt,
    vcmt_list,
    vedio_like
)
from frontend.api_v1.user_info import (
    get_user_info,
    update_userif,
    update_password,
    update_phone,
    my_blog,
    my_question,
    focus_other,
    my_focus_list,
    focus_me_list,
    get_my_wallet,
    wallet_record,
    create_withdraw_source,
    withdraw_source_list,
    withdraw_apply,
    coin_change,
    update_photo
)
from frontend.api_v1.index import get_index
from frontend.api_v1.common import (
    help_list,
    help_detail,
    version_info
)


urlpatterns: List[Any] = [
    path(r'get_index', get_index, name='get_index'),

    # 登陆注册模块
    path(r'sms_send', sms_send, name='sms_send'),
    path(r'sms_check', sms_check, name='sms_check'),
    path(r'login', login, name='login'),
    path(r'register', register, name='register'),
    path(r'forget', forget, name='forget'),
    path(r'logout', logout, name='logout'),

    # 博客模块
    path(r'blog_cat', blog_cat, name='blog_cat'),
    path(r'blog_list', blog_list, name='blog_list'),
    path(r'blog_detail', blog_detail, name='blog_detail'),
    path(r'comment_list', comment_list, name='comment_list'),
    path(r'blog_like', blog_like, name='blog_like'),
    path(r'create_cmt_reply', create_cmt_reply, name='create_cmt_reply'),
    path(r'cmt_reply_like', cmt_reply_like, name='cmt_reply_like'),

    # 问答模块
    path(r'question_cat', question_cat, name='question_cat'),
    path(r'create_question', create_question, name='create_question'),
    path(r'question_list', question_list, name='question_list'),
    path(r'question_detail', question_detail, name='question_detail'),
    path(r'question_reply', question_reply, name='question_reply'),
    path(r'create_reply', create_reply, name='create_reply'),
    path(r'qs_comment_like', qs_comment_like, name='qs_comment_like'),

    # 教程模块
    path(r'cource_list', cource_list, name='cource_list'),
    path(r'cource_detail', cource_detail, name='cource_detail'),
    path(r'cource_article', cource_article, name='cource_article'),
    path(r'create_ca_cmt', create_ca_cmt, name='create_ca_cmt'),
    path(r'cmt_list', cmt_list, name='cmt_list'),

    # 视频模块
    path(r'vedio_list', vedio_list, name='vedio_list'),
    path(r'vedio_detail', vedio_detail, name='vedio_detail'),
    path(r'create_vcmt', create_vcmt, name='create_vcmt'),
    path(r'vcmt_list', vcmt_list, name='vcmt_list'),
    path(r'vedio_like', vedio_like, name='vedio_like'),

    # 我的模块
    path(r'get_user_info', get_user_info, name='get_user_info'),
    path(r'update_userif', update_userif, name='update_userif'),
    path(r'update_password', update_password, name='update_password'),
    path(r'update_phone', update_phone, name='update_phone'),
    path(r'my_blog', my_blog, name='my_blog'),
    path(r'my_question', my_question, name='my_question'),
    path(r'focus_other', focus_other, name='focus_other'),
    path(r'my_focus_list', my_focus_list, name='my_focus_list'),
    path(r'focus_me_list', focus_me_list, name='focus_me_list'),
    path(r'get_my_wallet', get_my_wallet, name='get_my_wallet'),
    path(r'wallet_record', wallet_record, name='wallet_record'),
    path(r'create_withdraw_source', create_withdraw_source, name='create_withdraw_source'),
    path(r'withdraw_source_list', withdraw_source_list, name='withdraw_source_list'),
    path(r'withdraw_apply', withdraw_apply, name='withdraw_apply'),
    path(r'coin_change', coin_change, name='coin_change'),
    path(r'update_photo', update_photo, name='update_photo'),

    # 公共模块
    path(r'help_list', help_list, name='help_list'),
    path(r'help_detail', help_detail, name='help_detail'),
    path(r'version_info', version_info, name='version_info'),
]