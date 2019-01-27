# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 18:27
# @Author  : chengz
# @File    : adminx.py
# @Software: PyCharm
from xadmin import views
from .models import UserInfo
import xadmin


class UserInfoAdmin(object):
    list_display = ('id', 'username', 'nick_name', 'birthday', 'gender', 'mobile', 'email', 'address', 'last_login')
    search_fields = ('username',)


xadmin.site.unregister(UserInfo)
xadmin.site.register(UserInfo, UserInfoAdmin)

