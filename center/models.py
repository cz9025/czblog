# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


# 这个是在自带的认证表上添加字段
class UserInfo(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='匿名')
    # 生日的类型改为字符串的了
    birthday = models.CharField(max_length=20, null=True, blank=True, verbose_name='生日', default='2018-01-01')
    gender = models.CharField(max_length=6, choices=(('1', '男'), ('0', '女')), default='0', verbose_name='性别')
    address = models.CharField(max_length=100, null=True, blank=True, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, default='',verbose_name='手机号')
    head_img = models.ImageField(upload_to='img', verbose_name='头像', null=True, blank=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
