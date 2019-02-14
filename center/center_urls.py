# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    # 我的资料
    # url(r'^(?P<use>.*?)$', views.centers, name='mycenter'),
    url(r'^(?P<name>.*?)$', views.usercenter, name='usercenter'),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
