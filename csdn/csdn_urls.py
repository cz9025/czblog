# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 22:17
# @Author  : cz9025
# @File    : csdn_urls.py
# @Software: PyCharm

from django.conf.urls import url
from . import views

urlpatterns = [

    # 首页
    url(r'', views.index, name='index'),
    # url(r'^(?P<dataurl>.*?)$', views.details, name='details'),


]