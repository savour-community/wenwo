# encoding=utf-8

import re
from django import forms
from scauth.models import AuthUser
from django.core.files.base import ContentFile


class UpdateUifForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        label="用户名",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入用户名", "class": "el-input"}
        ),
        error_messages={"required": "请输入用户名, 用户名不能为空"},
    )
    photo = forms.ImageField(required=False)
    user: AuthUser

    class Meta:
        model = AuthUser
        fields = [
            'name', 'photo'
        ]

    def __init__(self, request, user: AuthUser, *args, **kw):
        self.request = request
        self.user = user
        super(UpdateUifForm, self).__init__(*args, **kw)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user = AuthUser.objects.filter(name=name).first()
        if user is not None and name != user.name:
            raise forms.ValidationError('该用户名在系统中已经存在, 请选择其他的用户名')
        return name

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        return photo

    def save_user_info(self):
        try:
            file_content = ContentFile(self.request.FILES['photo'].read())
            self.user.photo.save(self.request.FILES['photo'].name, file_content)
        except:
            pass
        self.user.name = self.clean_name()
        self.user.save()

