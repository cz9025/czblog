# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
import models
import logging


def index(request):
    """首页"""
    old_url = request.get_full_path()
    # arg_urls = request.get_full_path()
    # print "===index=get_full_path===", old_url
    logging.log(logging.INFO,'old_url=>>>'+old_url)
    # s = request.build_absolute_uri()
    # print "index=>s=>>>>>",s
    index_urls = request.path
    print "index=>>index_urls=>>>>",index_urls
    blogs = models.Blogs.objects.all().order_by('-tops', '-ctime')  # [0:10]
    # print blogs
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

    # locals()函数会以字典类型返回当前位置的全部局部变量。
    return render(request, 'blog/index.html', locals())


def search(request):
    """主页搜索  增加翻页"""
    title = request.GET.get('title')
    s = request.build_absolute_uri()
    print "s=>>>>>",s
    arg_urls = request.path[0:-1] + "?title=" + title
    print "arg_urls=>>>>",arg_urls

    # 增加翻页
    blogs = models.Blogs.objects.filter(title__contains=title).order_by('-tops', '-ctime')

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

    return render(request, 'blog/index.html', locals())


def error(request):
    """错误页面"""
    return render(request, 'error.html')


def blog_page(request, blog_id):
    """博客详情页面"""
    # return HttpResponse(6)
    if not request.user.is_authenticated:
        return redirect('/login/')
    # blog=None
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/czblog')
    try:
        blog = models.Blogs.objects.get(id=blog_id)
        # 阅读量+1
        blog.rcount = blog.rcount + 1
        blog.save()
    except Exception, e:
        print 'blog_page==>>>>error>>>>>', e
        return render(request, 'error.html')

    # 评论
    if request.POST:
        blog = models.Blogs.objects.get(id=blog_id)
        # blogs = request.POST.get('blog_id')
        comms = request.POST.get('comment')
        uses = request.user
        models.Comments.objects.create(uses=uses, comms=comms, cbid=blog_id, cblog=blog.title)
        #
        # counts = models.Comments.objects.filter(cbid=blog_id).count()
        blog.coms += 1
        blog.save()
        # print "=================提交评论成功================="
        # 这个只能用重定向，不然刷新页面还会提交
        print 'pinglun===url=>>>>', request.path
        # return redirect(request.path)
        return redirect('blog:blog_page', blog_id)
        # return redirect('/blog/%s' % blog_id)

    # 评论显示,按博客的id查询
    comm = models.Comments.objects.filter(cbid=blog_id).order_by('-ctime')

    # 区分自己的和别人的博客uses
    # name = request.user
    # if name == blog.uname:
    #     return render(request, 'blog/blog_page.html', {'blog': blog, 'comm': comm})

    return render(request, 'blog_page.html', {'blog': blog, 'comm': comm})


def ulike(request, blog_id):
    """点赞"""
    # if request.GET:
    # 判断当前用户是否点赞

    if not request.user.is_authenticated:
        return redirect('/login/')

    name = request.user
    islike = models.Likes.objects.filter(like_user=name, like_id=blog_id).count()
    print ("dianzan::::::::", islike)
    # 该用户有点赞时
    if islike:
        return HttpResponse("2")
    # 该用户没有点赞时
    else:
        blike = models.Blogs.objects.get(id=blog_id)
        blike.like = blike.like + 1
        blike.save()
        # 保存谁点赞的
        models.Likes.objects.create(like_user=name, like_title=blike.title, like_id=blog_id)
        return HttpResponse("1")


def del_comms(request, blog_id):
    """删除自己的评论"""
    delId = request.GET.get("id")
    print ("delid===", delId)
    models.Comments.objects.filter(id=delId).delete()
    #
    blog = models.Blogs.objects.get(id=blog_id)
    # counts = models.Comments.objects.filter(cbid=blog_id).count()
    # print ("del_comms===", counts)
    # 有删除评论的话，直接在博客表中的评论数减1就行了；不需要再去查评论表
    blog.coms -= 1
    blog.save()

    return HttpResponse(1)


def compage(request, blog_id):
    """博客详情页面，评论翻页       还没有做"""
    cpage = models.Comments.objects.filter(cbid=blog_id).order_by('-ctime')

    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(cpage, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        cpage = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        cpage = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        cpage = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, '/blog/%s' % blog_id, locals())


def marks(request, tags):
    """按标签"""
    blogs = models.Blogs.objects.filter(marks_id=tags).order_by('-tops', '-ctime')
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
    return render(request, 'blog/marks.html', locals())
