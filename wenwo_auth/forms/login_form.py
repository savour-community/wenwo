# encoding=utf-8

import re
from django import forms
from wenwo_auth.models import User
from django.core.cache import cache
from wenwo_auth.helper import hash_code


class UserPwdLoginForm(forms.Form):
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
            {"type": "password", "placeholder": "请输入密码", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入密码, 密码不能为空"},
    )

    def __init__(self,  request,  *args, **kw):
        self.request = request
        super(UserPwdLoginForm, self).__init__(*args, **kw)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone in ["", None]:
            raise forms.ValidationError('手机号码不能为空')
        user = User.objects.filter(phone=phone).first()
        if user is None:
            raise forms.ValidationError('用户不存在 请去注册')
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password in ["", None]:
            raise forms.ValidationError('密码不能为空')
        user = User.objects.filter(phone=self.cleaned_data.get('phone')).first()
        if user is None:
            raise forms.ValidationError('用户不存在 请去注册')
        if user.password != hash_code(password):
            raise forms.ValidationError('密码错误，请核对后输入')
        return password


class UserCodeLoginForm(forms.Form):
    phone = forms.CharField(
        required=True,
        label="手机号",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "手机号", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入手机号码, 手机号码不能为空"},
    )
    v_code = forms.CharField(
        required=True,
        label="验证码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "text", "placeholder": "请输入验证码", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入验证码, 验证码不能为空"},
    )

    def __init__(self, request,  *args, **kw):
        self.request = request
        super(UserCodeLoginForm, self).__init__(*args, **kw)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone in ["", None]:
            raise forms.ValidationError('手机号码不能为空')
        user = User.objects.filter(phone=phone).first()
        if user is None:
            raise forms.ValidationError('用户不存在 请去注册')
        return phone

    def clean_v_code(self):
        v_code = self.cleaned_data.get('v_code')
        if v_code in ["", None]:
            raise forms.ValidationError('验证码不能为空')
        if v_code != cache.get(self.cleaned_data.get('phone')):
            raise forms.ValidationError('验证码错误，请核对之后输入')
        return v_code




