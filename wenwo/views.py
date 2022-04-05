from django.shortcuts import render
from wenwo.models import Link
from wenwo_auth.models import User, UserInfo


def global_variable(request):
    is_login = request.session.get('is_login')
    if is_login is True:
        uid = int(request.session.get('user_id'))
        user = User.objects.filter(id=uid).first()
        if user is not None:
            g_user_info = UserInfo.objects.filter(user_id=user.id).first()
        else:
            g_user_info = None
    else:
        g_user_info = None
    link_list = Link.objects.all().order_by('-id')[:100]
    return locals()


