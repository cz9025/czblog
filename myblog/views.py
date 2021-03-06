# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from markdown import markdown

# 我的博客
from blog.models import Bmarks, Blogs, Comments
from czblog import settings


def userblog(request):
    """我的博客"""
    # return HttpResponse('userblog')
    # 如果没登录就需先登录
    if not request.user.is_authenticated:
        return redirect('/login/')
    # 获取登录的用户名
    name = request.user

    # 增加翻页
    blogs = Blogs.objects.filter(uname=name).order_by('-tops', '-ctime')

    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(blogs, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        blogs = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        blogs = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'myblog/userblog.html', locals())


def mysearch(request):
    """我的博客搜索"""
    # return HttpResponse('mysearch')
    if not request.user.is_authenticated:
        return redirect('/login/')
    name = request.user
    title = request.GET.get('title')
    arg_urls = request.path + "?title=" + title
    print ("mysearch=>>>",arg_urls)
    # 增加翻页
    blogs = Blogs.objects.filter(uname=name, title__contains=title).order_by('-tops', '-ctime')
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(blogs, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        blogs = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        blogs = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'myblog/userblog.html', locals())


def edit_blog(request):
    """编辑博客"""
    # return HttpResponse('edit_blog')
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.GET:
        blog_id = request.GET.get('id', 0)
        if blog_id == 0:
            return render(request, 'error.html')
        # 当博客被删除后，再点击编辑时，能获取到id值，但是再数据库查询时，就没有了
        try:
            blog = Blogs.objects.get(id=blog_id)
            marks = Bmarks.objects.all()
            return render(request, 'myblog/edit_blog.html', {'blog': blog, 'marks': marks})
        except Exception, e:
            print '===enter blog error===', e
            return render(request, 'error.html')

    if request.POST:
        print '==========post requests=========='
        blog_id = request.POST.get('id', 0)
        title = request.POST.get('title', 0)
        content = request.POST.get('content', 0)
        tags = request.POST.get('tags')
        # print '===>>>>>>>', content
        # print '===>>>>>>>', markdown(content)

        # 如果博客存在，则判断
        # if Blogs.objects.filter(title=title) and oldtitle != title:
        #     marks = Bmarks.objects.all()
        #     message = '该博客标题已存在，修改标题重新发布吧！'
        #     return render(request, 'myblog/add_blog.html',
        #                   {'message': message, 'marks': marks, 'title': title, 'tags': tags, 'content': content})
        # 保存时，发现文章没找到则显示错误的页面
        try:
            print '====post blog id=>>>>', blog_id
            article = Blogs.objects.get(id=blog_id)
            article.title = title
            article.content = markdown(content)
            article.marks_id = tags
            article.save()

        except Exception, e:
            print '===submit blog error===>>>>', e
            return render(request, 'error.html')
        return redirect('/myblog/')


def add_blog(request):
    """增加博客"""
    if not request.user.is_authenticated:
        return redirect('/login/')
    name = request.user
    if request.POST:
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags','0')
        newmarks=request.POST.get('newmarks',0)
        if newmarks:
            # tags=newmarks
            mark=Blogs.objects.values('marks_id').distinct()
            print "当前用户所有的标记=>>>>>>",mark
        else:
            print "00000=%s=00000"%(newmarks)

        # 非空判断title   content
        # if not title:
        #     marks = Bmarks.objects.all()
        #     return render(request, 'myblog/add_blog.html', {'message': '标题', 'marks': marks})

        # 如果博客存在，则判断
        if Blogs.objects.filter(title=title).count():
            marks = Bmarks.objects.all()
            message = '该标题已存在'
            return render(request, 'myblog/add_blog.html',
                          {'message': message, 'marks': marks, 'title': title, 'tags': tags, 'content': content})

        Blogs.objects.create(title=title, content=markdown(content), marks_id=tags, uname_id=name)
        # 添加完成重定向到我的博客
        return redirect('/myblog/')
    marks = Bmarks.objects.all()
    return render(request, 'myblog/add_blog.html', {'marks': marks})


# 删除博客  也要像编辑那样判断
def del_blog(request):
    if request.GET:
        blog_id = request.GET.get('id', 0)
        print ('del_blog===要删除博客的id======', blog_id)
        if blog_id == 0:
            print ('del_blog=== 为0则没有找到该博客 ========= ', blog_id)
            return render(request, 'error.html')
        # 当博客被删除后，再点删除时，就显示错误页面
        try:
            Blogs.objects.get(id=blog_id).delete()
            Comments.objects.filter(cbid=blog_id).delete()
            return redirect('/myblog/')
        except:
            print ('del_blog==没有找到博客')
            return render(request, 'error.html')


# 按标签
def marks(request, name, tags):
    # return HttpResponse('marks')
    if not request.user.is_authenticated:
        return redirect('/login/')
    # name = request.user
    blogs = Blogs.objects.filter(uname=name, marks_id=tags).order_by('-tops', '-ctime')
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(blogs, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        blogs = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        blogs = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'myblog/marks.html', locals())


def uploadImg(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    name = request.user
    img = request.FILES['editormd-image-file']
    path='%s/article/%s' % (settings.MEDIA_ROOT,name)
    isExists=os.path.exists( path)
    print isExists
    if not isExists:
        os.makedirs(path)

    print 'user.head_img=>>>>', img
    # 上传文件
    fname = '%s/%s' % (path, img)
    print 'fname=>>>', fname
    with open(fname, 'wb') as pic:
        for c in img.chunks():
            pic.write(c)

    res = {
        'success': 1,
        'message': "上传成功！",
        # 'url': fname,
        'url': '/media/article/%s/%s' % (name,img),
    }
    return JsonResponse(res)
