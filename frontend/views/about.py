#encoding=utf-8

import logging
from django.shortcuts import render
from django.shortcuts import redirect


def download(request):
    nav_cat = "download"
    return render(request, 'v2_front/about/download.html', locals())
