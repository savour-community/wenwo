#encoding=utf-8

from django import forms


class UserPhotoForm(forms.Form):
    user_pho = forms.ImageField(label="用户头像")

    def __init__(self, *args, **kw):
        super(UserPhotoForm, self).__init__(*args, **kw)



class UserInfoForm(forms.Form):
    user_real_name = forms.CharField(label="真实名字", max_length=64)
    user_intro = forms.CharField(label="简介", max_length=64)
    user_sex = forms.CharField(label="性别", max_length=64)
    user_age = forms.CharField(label="年龄", max_length=64)
    user_pos = forms.CharField(label="职位", max_length=64)
    college = forms.CharField(label="学校", max_length=64)
    education = forms.CharField(label="学历", max_length=64)
    company = forms.CharField(label="公司", max_length=64)
    industry = forms.CharField(label="行业", max_length=64)
    start_work = forms.CharField(label="开始工作时间", max_length=64)
    user_card = forms.CharField(label="身份证", max_length=64)
    user_email = forms.CharField(label="邮件", max_length=64)
    user_qq = forms.CharField(label="QQ", max_length=64)
    user_wechat = forms.CharField(label="微信", max_length=64)

    def __init__(self, *args, **kw):
        super(UserInfoForm, self).__init__(*args, **kw)