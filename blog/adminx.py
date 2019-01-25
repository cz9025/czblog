# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 15:16
# @Author  : chengz
# @File    : xadmin.py
# @Software: PyCharm


from .models import Blogs, Bmarks, Comments, Likes
from xadmin import views
import xadmin


class BlogsAdmin(object):
    list_display = ('id', 'title', 'tops', 'rcount', 'coms', 'like', 'uname', 'marks', 'ctime')
    search_fields = ('title',)
    date_hierarchy = 'ctime'
    # ordering = ('ctime',)
    # fields = ('title','coms')   # 在后台编辑博客时，只能修改这些字段


xadmin.site.register(Blogs, BlogsAdmin)


class BmarksAdmin(object):
    list_display = ('tags',)
    search_fields = ('tags',)


xadmin.site.register(Bmarks, BmarksAdmin)


class CommentsAdmin(object):
    list_display = ('comms', 'cblog', 'uses')
    search_fields = ('comms',)


xadmin.site.register(Comments, CommentsAdmin)


class LikesAdmin(object):
    list_display = ('like_user', 'like_title')
    search_fields = ('like_title',)


xadmin.site.register(Likes, LikesAdmin)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = "czblog后台管理"
    site_footer = "cz9025的网站"


xadmin.site.register(views.CommAdminView, GlobalSetting)
