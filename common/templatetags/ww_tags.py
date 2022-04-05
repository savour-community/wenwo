#encoding=utf-8

from urllib.parse import urljoin
import pytz
import json
from django.conf import settings
from django import template
from django.contrib.contenttypes.models import ContentType
from common.helpers import vformat, utc2str, d0, dec
from wenwo_auth.models import User, UserInfo


register = template.Library()


@register.filter(name='vformat')
def decimal_format(value):
    return vformat(value)


@register.filter(name='hdatetime')
def repr_datetime(value):
    if not value:
        return ''
    tz = pytz.timezone(settings.TIME_ZONE)
    return utc2str(value.astimezone(tz), "%Y-%m-%d %H:%M:%S")


@register.filter(name='hdate')
def repr_date(value):
    if not value:
        return ''
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime("%Y-%m-%d")


@register.filter(name='username')
def username(value):
    if not value:
        return ''
    user = User.objects.get(id=value)
    return user.user_name


@register.filter(name='userinfoimg')
def user_info_img(value):
    if not value:
        return ''
    user_info = UserInfo.objects.filter(user_id=value).first()
    if user_info is not None:
        return user_info.user_pho
    else:
        return ''


@register.filter(name='userinfopos')
def userinfopos(value):
    if not value:
        return ''
    user_info = UserInfo.objects.filter(user_id=value).first()
    if user_info is None:
        return "高级研发工程师"
    else:
        return user_info.user_pos


@register.filter(name='userinfo_introduce')
def userinfo_introduce(value):
    if not value:
        return ''
    user_info = UserInfo.objects.filter(user_id=value).first()
    if user_info is None:
        return "暂无介绍"
    else:
        return user_info.user_intro


@register.filter(name="keep_two_decimal_places")
def ktd_places(value):
    if value in ["", None, "None", 0, d0]:
        return "0"
    dec_value = dec(value).quantize(dec("0.00"))
    return (
        dec_value.to_integral()
        if dec_value == dec_value.to_integral()
        else dec_value.normalize()
    )


@register.filter(name="is_checked")
def is_checked(value):
    return {
        'Yes': '已审核',
        'No': '未审核',
    }.get(value, '')

@register.filter(name="coin_type")
def coin_type(value):
    return {
        'WenwoCoin': '问我积分',
        'Cny': '人民币',
    }.get(value, '')


@register.filter(name="wallet_type")
def wallet_type(value):
    return {
        'Withdraw': '提现',
        'Reward': '平台奖励',
        'Deposit': '充值',
        'Register': '注册赠送',
    }.get(value, '')


@register.filter(name="source_type")
def source_type(value):
    return {
        'Register': '注册赠送',
        'InviteReward': '邀请奖励',
        'WeiChat': '微信',
        'ZhiFuBao': '支付宝',
        'BlogReward': '写博客奖励',
        'QuestionReward': '问题奖励',
        'AnswerReward': '回答问题奖励',
        'CourseReward': '专栏课程奖励',
        'VideoReward': '视频教程奖励',
        'FeedBackReward': '反馈问题奖励'
    }.get(value, '')


@register.filter(name="feedback_status")
def feedback_status(value):
    return {
        'Accept': '您的意见被小问采纳',
        'Refuse': '您的意见不合适小问，欢迎继续提出反馈',
        'UnHandle': '您的意见还未被小问看见'
    }.get(value, '')


@register.filter(name="check_status")
def check_status(value):
    return {
        'Checking': '审核中',
        'CheckFail': '审核失败',
        'CheckPass': '审核通过',
    }.get(value, '')
