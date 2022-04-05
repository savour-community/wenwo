# encoding=utf-8

import re
import base64
from django import forms
from wenwo_auth.models import (
    User,
    UserInfo,
    UserWallet,
    UserWalletRecord
)
from django.core.cache import cache
from common.helpers import dec
from wenwo_auth.helper import hash_code


class UserRegisterForm(forms.Form):
    phone = forms.CharField(
        required=True,
        label="手机号",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "手机号", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入手机号码, 手机号码不能为空"},
    )
    password = forms.CharField(
        required=True,
        label="密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入密码, 数字字母均可以长度大于8位小于20位", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入密码, 密码不能为空"},
    )
    c_password = forms.CharField(
        required=True,
        label="密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入确认密码", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入确认密码, 确认密码不能为空"},
    )
    v_code = forms.CharField(
        required=True,
        label="验证码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "text", "placeholder": "请输入验证码", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入验证码， 验证码不能为空"},
    )
    invite_code=forms.CharField(
        required=False,
        label="邀请码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "text", "placeholder": "请输入邀请码(选填)", "class": "el-input__inner"}
        )
    )

    def __init__(self, request, *args, **kw):
        self.request = request
        super(UserRegisterForm, self).__init__(*args, **kw)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone in ["", None]:
            raise forms.ValidationError('手机号码不能为空')
        user_exist = User.objects.filter(phone=phone).first()
        if user_exist is not None:
            raise forms.ValidationError('该手机号已被注册, 请直接去登陆')
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password in ["", None]:
            raise forms.ValidationError('密码不能为空')
        if not re.match('''[-`=\\\[\];',./~!@#$%^&*()_+|{}:"<>?A-Za-z0-9]{8,}$''', password):
            raise forms.ValidationError('密码设置不符合要求，需要大于8位, 可以是数字，字母和字符的组合')
        return password

    def clean_c_password(self):
        password = self.clean_password()
        c_password = self.cleaned_data.get('c_password')
        if c_password in ["", None]:
            raise forms.ValidationError('确认密码不能为空')
        if password != c_password:
            raise forms.ValidationError('两次输入的密码不一样')
        return c_password

    def clean_v_code(self):
        v_code = self.cleaned_data.get('v_code')
        if v_code in ["", None]:
            raise forms.ValidationError('验证码不能为空')
        if v_code != cache.get(self.cleaned_data.get('phone')):
            raise forms.ValidationError('验证码不正确')
        return v_code

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        if invite_code not in ["", None, "None"]:
            user = User.objects.filter(invite_code=invite_code).first()
            if user is None:
                raise forms.ValidationError('系统内部没有这个邀请码')
            else:
                return invite_code
        else:
            return invite_code

    def save_register_user(self):
        invite_code = self.clean_invite_code()
        if invite_code not in ["", None, "None"]:
            user = User.objects.filter(invite_code=invite_code).first()
            invite_user_id = user.id
            user_wallet = UserWallet.objects.filter(
                user=user,
                coin_type="WenwoCoin"
            ).first()
            user_wallet.amount += 100
            user_wallet.save()
            UserWalletRecord.objects.create(
                user=user,
                amount=dec('100'),
                coin_type="WenwoCoin",
                source_type="InviteReward",
                wallet_type="Reward",
            )
        else:
            invite_user_id = 0
        bs = base64.b64encode(self.clean_phone().encode("utf-8"))
        create_user = User.objects.create(
            user_name="小问",
            phone=self.clean_phone(),
            password=hash_code(self.clean_password()),
            invite_user_id=invite_user_id,
            invite_code=bs.decode()
        )
        create_user_info = UserInfo.objects.create(
            user_id=create_user.id
        )
        UserWallet.objects.create(
            user=create_user,
            coin_type="Cny"
        )
        UserWallet.objects.create(
            user=create_user,
            coin_type="WenwoCoin",
            amount=dec('100')
        )
        UserWallet.objects.create(
            user=create_user,
            coin_type="Cny",
            amount=dec('0')
        )
        UserWalletRecord.objects.create(
            user=create_user,
            amount=dec('100'),
            coin_type="WenwoCoin",
            source_type="Register",
            wallet_type="Reward",
        )
        return create_user






