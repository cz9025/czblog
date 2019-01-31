# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
import requests


def index(request):
    return render(request, 'interface/interface.html')


def interface_get(request):
    print "interface_get   =>>>>>"
    if request.POST:
        urls = request.POST.get('urls')
        print "params=>>>接收到的参数：=>>>", type(request.POST.get('datas'))
        # 参数有中文会报错
        params = str(request.POST.get('datas'))
        print "params=>>>处理过的参数：=>>>", params
        user_agent = request.POST.get('user_agent', '')
        print "user_agent=>>>", user_agent
        content_type = request.POST.get('content_type', 'text/html')
        print "content_type=>>>", content_type

        headers = {'Content-Type': content_type, 'User-Agent': user_agent}

        # 请求方式 1 get   2 post
        mode = request.POST.get('mode', 1)
        # print "mode=>>>",type(mode)
        if mode == '1':
            print u"本次使用get请求"
            response = requests.get(url=urls, params=params, headers=headers)
        else:
            print u"本次使用post请求"
            response = requests.post(url=urls, params=params, headers=headers)

        print "response.url=>>>>", response.url
        print "response.encoding=>>>", response.encoding

        resp = {'status': 10000, 'data': response.text}
        print "resp=>>>", resp

        return JsonResponse(resp)
        # print title
    return render(request, 'interface/interface.html')
