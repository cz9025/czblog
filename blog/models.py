# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime
# from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import AbstractUser

from center.models import UserInfo

# 分类表
class Bmarks(models.Model):
    id = models.AutoField(max_length=10, primary_key=True)
    tags = models.CharField(max_length=128, unique=True, null=False, verbose_name="标签")

    def __str__(self):
        return self.tags.encode('utf-8')

    class Meta:
        db_table = 'blog_marks'
        unique_together = ('tags',)
        verbose_name = "分类"
        verbose_name_plural = "分类"

# Create your models here.
class Blogs(models.Model):
    id = models.AutoField(max_length=10, primary_key=True)
    title = models.CharField(max_length=128, unique=True, verbose_name="标题")
    # content = models.CharField(max_length=256)
    content = models.TextField(verbose_name="内容")
    # 阅读量
    rcount = models.IntegerField(default=0, verbose_name="阅读量")
    # 评论数
    coms = models.IntegerField(default=0, verbose_name="评论数")
    # 点赞数
    like = models.IntegerField(default=0, verbose_name="点赞数")
    # 创建时间
    ctime = models.DateTimeField(max_length=30, auto_now_add=True, null=False, verbose_name="创建时间")
    # 最后修改时间
    utime = models.DateTimeField(max_length=30, auto_now=True, null=False, verbose_name="修改时间")

    marks = models.ForeignKey(Bmarks, null=True, on_delete=models.SET_DEFAULT, related_name='blog_marks',
                              to_field='tags', default="未分类", verbose_name="分类")
    uname = models.ForeignKey(UserInfo, null=True, on_delete=models.SET_DEFAULT,
                              to_field='username', default='匿名', verbose_name="用户名")
    # 是否置顶
    tops = models.IntegerField(default=0, choices=((1, '是'), (0, '否')), verbose_name="置顶")

    def __str__(self):
        return self.title.encode('utf-8')

    class Meta:
        db_table = 'user_blogs'
        unique_together = ('title',)
        verbose_name = "博客"
        verbose_name_plural = "博客"






# 评论表
class Comments(models.Model):
    id = models.AutoField(max_length=10, primary_key=True)
    # 博客相关的id
    cbid = models.IntegerField(null=True, verbose_name="博客id")
    # 博客的标题
    cblog = models.CharField(max_length=128, null=True, verbose_name="博客标题")
    # 评论的内容
    comms = models.TextField(max_length=300, verbose_name="评论内容")
    # 评论人  直接在views中获取当前登录的用户，保存起来
    uses = models.CharField(max_length=128, blank=False, default='匿名', verbose_name="评论人")
    # 创建时间
    ctime = models.DateTimeField(max_length=30, auto_now_add=True, null=True, verbose_name="创建时间")

    # 博客删除后，评论跟着删除
    # cblog = models.ForeignKey(Blogs, null=True, on_delete=models.SET_DEFAULT, related_name='user_blogs',
    #                           to_field='title', default="该博客已删除")

    # uses = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='auth_user', to_field='id')

    def __str__(self):
        return self.comms.encode('utf-8')

    class Meta:
        db_table = 'use_comments'
        verbose_name = "评论"
        verbose_name_plural = "评论"


# 点赞表
class Likes(models.Model):
    id = models.AutoField(max_length=10, primary_key=True)
    # 点赞人
    like_user = models.CharField(max_length=128, blank=False, default='匿名', verbose_name="点赞人")
    # 被赞的文章title
    like_title = models.CharField(max_length=128, verbose_name="被赞文章")
    # 被赞文章的id
    like_id = models.IntegerField(null=True, verbose_name="被赞文章id")
    # 点赞时间
    like_time = models.DateTimeField(max_length=30, auto_now_add=True, null=False, verbose_name="点赞时间")

    def __str__(self):
        return self.like_title.encode('utf-8')

    class Meta:
        db_table = 'blog_like'
        verbose_name = "点赞"
        verbose_name_plural = "点赞"


