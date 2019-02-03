# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 18:27
# @Author  : chengz
# @File    : adminx.py
# @Software: PyCharm

from .models import UserInfo
import xadmin


class UserInfoAdmin(object):
    list_display = ('id', 'username', 'nick_name', 'birthday', 'gender', 'mobile', 'email', 'address', 'last_login')
    search_fields = ('username',)
    list_per_page = 20


xadmin.site.unregister(UserInfo)
xadmin.site.register(UserInfo, UserInfoAdmin)


# 图表   没起作用
class ReporDataAdmin(object):
    list_display = ('year', 'cn')
    list_per_page = 20
    data_charts = {
        "user_count": {'title': u"User Register Raise", "x-field": "day", "y-field": ("cn",),
                       # "order": ('day',)
                       },
    }
