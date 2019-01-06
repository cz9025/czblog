# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
import requests


# Create your views here.


def index(request):
    return render(request, 'interface/interface.html')


def interface_get(request):
    if request.POST:
        urls = request.POST.get('urls')
        params = request.POST.get('datas')
        headers = request.POST.get('headers', {'Content-Type': 'text/html'})

        # headers = {'Content-Type': 'text/html'}
        response = requests.get(url=urls, params=params, headers=headers)
        print response.url

        print response.encoding
        resp = {'status': 10000, 'data': response.text.encode(response.encoding)}

        return JsonResponse(resp)
        # print title
    return render(request, 'interface/interface.html')
