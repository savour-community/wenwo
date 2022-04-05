# -*- coding: utf-8 -*-

import pytz
from django.db import models
from wenwo.models import BaseModel
from common.model_fields import IdField, DecField
from django.conf import settings
from common.helpers import dec, d0


tz = pytz.timezone(settings.TIME_ZONE)


SEX_CHOICES = [(x, x) for x in ['男', '女', '未知']]
COIN_TYPE_CHOICES = [(x, x) for x in ['Cny', 'WenwoCoin']]
SOURCE_CHANNEL = [(x, x) for x in [
        'WeiChat',
        'ZhiFuBao',
        'InviteReward',
        'Register',
        'BlogReward',
        'QuestionReward',
        'AnswerReward',
        'CourseReward',
        'VideoReward',
        'FeedBackReward'
        'Output'
    ]
]

CHECK_CHOICE = [(x, x) for x in ['UnCheck', 'Checking', 'Checked', 'Refuse']]
WALLET_TYPE = [(x, x) for x in ['Deposit', 'Withdraw', "Reward", "Register"]]
IS_PAY = [(x, x) for x in ['Yes', 'No']]
IS_DEL_CHOICES = [(x, x) for x in ['Yes', 'No']]
WITHDRAW_TYPE = [(x, x) for x in ['WeiChat', 'ZhiFuBao']]
EXPIRE_TYPE_CHOICES = [(x, x) for x in ['EXPIRED', 'UNEXPIRE']]
BackendAccountType = [(x, x) for x in ['Admin', "Outer", 'Inner']]
ValidSelect = [(x, x) for x in ['Yes', 'No']]


class ApiAuth(BaseModel):
    EXPIRE_CHOICES = [(x, x) for x in ['YES', 'NO']]
    STATUS_CHOICES = [(x, x) for x in ['UnVerify', 'Verifing', 'Verified']]
    name = models.CharField(
        max_length=64,
        default='',
        verbose_name="接入名称"
    )
    api_token = models.CharField(
        max_length=128,
        default='unknown',
        verbose_name="接入 api Token"
    )
    is_expire = models.CharField(
        max_length=128,
        default="NO",
        choices=EXPIRE_CHOICES,
        verbose_name="Token是否过期"
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='checking',
        verbose_name="API 审核状态"
    )

    class Meta:
        verbose_name = "API 授权表"
        verbose_name_plural = "API 授权表"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "api_token": self.api_token,
            "is_expire": self.is_expire,
            "status":self.status,
        }


class Account(BaseModel):
    name = models.CharField(max_length=32, unique=True)
    role = models.CharField(
        max_length=128,
        choices=BackendAccountType,
        default="Admin",
        verbose_name=u'账户角色'
    )
    password = models.CharField(
        max_length=128,
        default='',
        verbose_name=u'密码'
    )
    valid = models.CharField(
        max_length=128,
        choices=ValidSelect,
        default="Yes",
        verbose_name=u'是否有效'
    )

    class Meta:
        verbose_name = '后台用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "role": self.role,
            "valid": self.valid,
        }


class User(BaseModel):
    user_name = models.CharField(
        max_length=32,
        default='',
        verbose_name=u'用户名'
    )
    password = models.CharField(
        max_length=128,
        default='',
        verbose_name=u'密码'
    )
    token = models.CharField(
        max_length=256,
        default='',
        verbose_name=u'令牌'
    )
    token_is_expire = models.CharField(
        max_length=32,
        default="UNEXPIRE",
        choices=EXPIRE_TYPE_CHOICES,
        verbose_name=u'token是否过期'
    )
    phone = models.CharField(
        max_length=16,
        default='',
        verbose_name=u'手机号码'
    )
    is_sign = models.CharField(
        max_length=16,
        choices=IS_DEL_CHOICES,
        default='No',
        verbose_name=u'是否签约'
    )
    loginip = models.CharField(
        max_length=128,
        default='',
        verbose_name=u'登陆IP'
    )
    invite_user_id = IdField(
        default='0',
        db_index=True
    )
    invite_code = models.CharField(
        max_length=128,
        default='',
        verbose_name=u'邀请码'
    )
    focus_num = models.IntegerField(
        default=0,
        verbose_name=u'关注的人数'
    )
    fans_num = models.IntegerField(
        default=0,
        verbose_name=u'粉丝数量'
    )
    login_times = models.IntegerField(
        default=0,
        verbose_name=u'登陆次数'
    )
    regtime = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name=u'注册时间'
    )
    logintime = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name=u'最近登陆时间'
    )

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_name

    def userif_to_dict(self):
        try:
            user_info = UserInfo.objects.filter(user_id=self.id).first()
            user_wallet_list = UserWallet.objects.filter(user__id=self.id)
            cyn_amount = 0
            wenwo_amount = 0
            for uw in user_wallet_list:
                if uw.coin_type == "Cny":
                    cyn_amount = uw.amount
                if uw.coin_type == "WenwoCoin":
                    wenwo_amount = uw.amount
            if user_info is not None:
                return {
                    "id": self.id,
                    "user_name": self.user_name,
                    "user_photo": str(user_info.user_pho),
                    "user_pos": user_info.user_pos,
                    "focus_num": self.focus_num,
                    "fans_num": self.fans_num,
                    "cny": cyn_amount,
                    "sex": user_info.user_sex,
                    "wenwo_coin": wenwo_amount,
                    "phone": self.phone,
                    "login_times": self.login_times,
                    "create_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
                }
        except:
            return {
                "id": self.id,
                "user_name": self.user_name,
                "user_photo": "",
                "user_pos": "高级区块链工程师",
                "focus_num": self.focus_num,
                "fans_num": self.fans_num,
                "cny": 0.00,
                "sex": "未知",
                "wenwo_coin": 0.00,
                "phone": self.phone,
                "login_times": self.login_times,
                "create_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
            }

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "token": self.token,
            "phone": self.phone,
            "login_times": self.login_times,
            "create_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }


class Fans(BaseModel):
    me = models.ForeignKey(
        User,
        related_name="me_user_fans",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=u'我自己'
    )
    fans = models.ForeignKey(
        User,
        related_name="fans_user_me",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=u'我的粉丝'
    )

    class Meta:
        verbose_name = "粉丝表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return ""

    def focus_me_dict(self):
        return {
            "id": self.id,
            "user": self.me.to_dict(),
        }

    def my_focus_dict(self):
        return {
            "id": self.id,
            "user": self.fans.to_dict(),
        }


class UserInfo(BaseModel):
    user_real_name = models.CharField(
        max_length=64,
        default='',
        verbose_name=u'真实姓名'
    )
    user_pho = models.ImageField(
        upload_to='user_img/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=u'用户头像'
    )
    user_intro = models.TextField(
        max_length=512,
        blank=True,
        default='',
        verbose_name=u'用户简介'
    )
    user_sex = models.CharField(
        max_length=16,
        choices=SEX_CHOICES,
        default='未知',
        verbose_name=u'用户性别'
    )
    user_age = models.CharField(
        max_length=16,
        default='0',
        verbose_name=u'用户年龄'
    )
    user_pos = models.CharField(
        max_length=16,
        default='',
        verbose_name=u'用户职位'
    )
    college = models.CharField(
        max_length=16,
        default='',
        verbose_name=u'毕业大学'
    )
    education = models.CharField(
        max_length=16,
        default='',
        verbose_name=u'学历'
    )
    company = models.CharField(
        max_length=16,
        default='',
        verbose_name=u'所在单位'
    )
    industry = models.CharField(
        max_length=16,
        default='',
        verbose_name=u'所在行业'
    )
    start_work = models.CharField(
        max_length=16,
        default='',
        verbose_name=u'开始工作时间'
    )
    user_card = models.CharField(
        max_length=64,
        default='',
        verbose_name=u'用户身份证'
    )
    user_email = models.CharField(
        max_length=128,
        default='',
        verbose_name=u'用户邮箱'
    )
    user_id = IdField(
        default='',
        db_index=True,
        verbose_name=u'用户ID'
    )
    user_qq = models.CharField(
        default='',
        max_length=128,
        verbose_name=u'QQ'
    )
    user_wechat = models.CharField(
        default='',
        max_length=128,
        verbose_name=u'用户微信'
    )

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_real_name

    def to_dict(self):
        return {
            "user_real_name": self.user_real_name,
            "user_pho": self.user_pho,
            "user_sex": self.user_sex,
            "user_intro": self.user_intro,
            "user_age": self.user_age,
            "user_card": self.user_card,
            "user_email": self.user_email,
            "user_id": self.user_id,
            "user_qq": self.user_qq,
            "user_wechat": self.user_wechat,
        }


class UserWallet(BaseModel):
    user = models.ForeignKey(
        User, related_name='user_wallet',
        null=True, blank=True, on_delete=models.CASCADE,
        verbose_name=u'用户信息'
    )
    coin_type = models.CharField(
        max_length=32, choices=COIN_TYPE_CHOICES, default='Cny',
        verbose_name=u'钱包类型'
    )
    amount = DecField(default=0, verbose_name=u'金额')
    is_del = models.CharField(
        max_length=16,
        choices=IS_DEL_CHOICES,
        default='No',
        verbose_name=u'是不是删除'
    )

    class Meta:
        verbose_name = "用户钱包表"
        verbose_name_plural = "用户钱包表"

    def to_dict(self):
        dec_value = dec('{:f}'.format(self.amount)).quantize(dec("0.00"))
        amount = dec_value.to_integral() if dec_value == dec_value.to_integral() else dec_value.normalize()
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'amount': amount,
            'is_del': self.is_del,
        }


class UserWalletRecord(BaseModel):
    user = models.ForeignKey(
        User, related_name='user_withdraw',
        null=True, blank=True, on_delete=models.CASCADE,
        verbose_name=u'用户信息'
    )
    amount = DecField(default=0, verbose_name=u'金额')
    coin_type = models.CharField(
        max_length=32, choices=COIN_TYPE_CHOICES, default='Cny',
        verbose_name=u'币种类型'
    )
    source_type = models.CharField(
        max_length=16, choices=SOURCE_CHANNEL,
        default='Register', verbose_name=u'渠道'
    )
    source_id = IdField(default='0', db_index=True)
    wallet_type = models.CharField(
        max_length=16, choices=WALLET_TYPE,
        default='Deposit', verbose_name=u'充提奖励类型'
    )
    check_status = models.CharField(
        max_length=16, choices=CHECK_CHOICE,
        default='Checking', verbose_name=u'审核状态'
    )
    is_pay = models.CharField(
        max_length=16, choices=IS_PAY,
        default='No', verbose_name=u'是否已支付'
    )
    is_del = models.CharField(
        max_length=16, choices=IS_DEL_CHOICES,
        default='No', verbose_name=u'是否删除'
    )

    class Meta:
        verbose_name = "用户资金记录表"
        verbose_name_plural = "用户资金记录表"

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'amount': self.amount,
            "coin_type": self.coin_type,
            "source_type": self.source_type,
            "source_id": self.source_id,
            'wallet_type': self.wallet_type,
            'check_status': self.check_status,
            'is_pay': self.is_pay,
            'is_del': self.is_del,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }


class WithdrawSource(BaseModel):
    user = models.ForeignKey(
        User, related_name='user_withdraw_source',
        null=True, blank=True, on_delete=models.CASCADE,
        verbose_name=u'用户信息'
    )
    wd_source = models.CharField(
        max_length=32, choices=WITHDRAW_TYPE, default='WeiChat',
        verbose_name=u'提现渠道'
    )
    account = models.CharField(
        max_length=200, blank=True,
        default='',
        verbose_name=u'提现账号'
    )
    qr_code = models.ImageField(
        upload_to='withdraw_img/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=u'二维码图片'
    )
    is_del = models.CharField(
        max_length=16, choices=IS_DEL_CHOICES,
        default='No', verbose_name=u'是不是删除')

    class Meta:
        verbose_name = "用户提现渠道表"
        verbose_name_plural = "用户提现渠道表"

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'wd_source': self.wd_source,
            'account': self.account,
            'qr_code': str(self.qr_code),
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }
