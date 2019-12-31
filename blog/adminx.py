# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 15:16
# @Author  : chengz
# @File    : xadmin.py
# @Software: PyCharm


from .models import Blogs, Bmarks, Comments, Likes
from center.adminx import UserInfo
from xadmin import views
import xadmin


class BlogsAdmin(object):
    list_display = ('id', 'title', 'tops', 'rcount', 'coms', 'like', 'uname', 'marks', 'ctime', 'tops')
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
    list_display = ('like_user', 'like_title', 'like_id', 'like_time')
    search_fields = ('like_title',)


xadmin.site.register(Likes, LikesAdmin)


class BaseSetting(object):
    enable_themes = True  # 开启主题使用
    use_bootswatch = True  # 开启主题选择  没有发现主题列表


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = "czblog后台管理"
    site_footer = "http://www.baidu.com"

    # menu_style="accordion"  #修改菜单栏 改成收缩样式

    # 设置models的全局图标
    global_search_models = [Blogs, UserInfo]
    global_models_icon = {
        UserInfo: "glyphicon glyphicon-user",
        Blogs: "glyphicon glyphicon-list-alt",
        Bmarks: "glyphicon glyphicon-tag",
        Likes: "glyphicon glyphicon-thumbs-up",
        Comments: "glyphicon glyphicon-leaf",

    }


xadmin.site.register(views.CommAdminView, GlobalSetting)
