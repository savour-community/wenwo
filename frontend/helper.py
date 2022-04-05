# encoding=utf-8

import json
from django.shortcuts import redirect


def check_user_login(func):
    def user_auth(request, *args, **kwargs):
        if request.session.get("is_login") is False \
                or request.session.get("is_login") is None:
            return redirect("login")
        return func(request, *args, **kwargs)
    return user_auth
