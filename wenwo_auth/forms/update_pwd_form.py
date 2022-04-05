# encoding=utf-8

import re
from django import forms
from scauth.models import AuthUser


class UpdatePasswordForm(forms.Form):
    old_passwrod = forms.CharField(
        required=True,
        label="老密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "原密码", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入原密码, 原密码不能为空"},
    )

    password = forms.CharField(
        required=True,
        label="密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入新密码", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入新密码, 新密码不能为空"},
    )

    c_password = forms.CharField(
        required=True,
        label="确认密码",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"type": "password", "placeholder": "请输入确认密码", "class": "el-input__inner"}
        ),
        error_messages={"required": "请输入确认密码, 确认密码不能为空"},
    )
    user: AuthUser

    class Meta:
        model = AuthUser
        fields = [
            'old_passwrod', 'passwrod', 'c_password'
        ]

    def __init__(self, user:AuthUser, request, *args, **kw):
        self.user = user
        self.request = request
        super(UpdatePasswordForm, self).__init__(*args, **kw)

    def clean_old_passwrod(self):
        old_passwrod = self.cleaned_data.get('old_passwrod')
        if old_passwrod in ["", None]:
            raise forms.ValidationError('老密码不能为空')
        if self.user.password != old_passwrod:
            raise forms.ValidationError('输入的老密码错误')
        return old_passwrod

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

    def update_password(self):
        self.user.password = self.clean_password()
        self.user.save()
