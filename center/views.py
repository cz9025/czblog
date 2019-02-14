# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth.models import User
import random
import string

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
# 改版后使用修改过的用户表，如果用自带的，记得注释这里
from czblog import settings
from .models import UserInfo
from django.core.files.base import ContentFile
# 自己的资料
from blog.models import Blogs


def usercenter(request, name):
    """查看资料"""
    print "usercenter start=====>>>>>>>>>>"
    if not request.user.is_authenticated:
        return redirect('/login/')
    # 查用户的信息,需要把用户的信息带过去
    user = UserInfo.objects.get(username=name)
    print type(user.birthday)
    print type(user.last_login)

    # 修改资料请求
    if request.POST:
        user.nick_name = request.POST.get('nick', '匿名')
        user.birthday = request.POST.get('birthday', '2018-01-01')
        user.address = request.POST.get('address', '')
        user.mobile = request.POST.get('mobile', '')
        # 性别要处理
        user.gender = request.POST.get('gender', 0)
        # 头像
        try:
            head_img = request.FILES['heads']

            print 'user.head_img=>>>>', head_img
            # 上传后的文件名就是自己的用户名
            user.head_img = user.username + '.png'
            # ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 12))
            fname = '%s/%s' % (settings.MEDIA_ROOT, user.head_img)
            print 'fname=>>>', fname
            with open(fname, 'wb') as pic:
                for c in head_img.chunks():
                    pic.write(c)

        except:
            print u'没有上传头像'

        user.save()
        # 修改资料后重定向，不然再次刷新会提示重新提交
        return redirect("center:usercenter", user.username)

    # arg_urls = request.path
    # print "arg_urls=>>>>", arg_urls

    # 增加翻页
    # 查询出该用户的博客
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

        # 该用户博客标签
    mark = {}
    for mk in blogs:
        if not mark.has_key(mk.marks_id):
            k = Blogs.objects.filter(uname=name, marks=mk.marks_id).count()

            mark[mk.marks_id] = k
            # print "biaoqian=======", mk.marks_id, len(k), mark

    print "<<<<<<<<<<=====usercenter end"
    return render(request, 'center/usercenter.html', locals())


def uselogin(request):
    """登录"""
    # if request.method == 'GET':
    # #     记住来源的url,如果没有则设置为首页('/blog')
    #     request.session['login_from'] = request.META.get('HTTP_REFERER', '/blog')
    #     print "===进入登录===",request.session['login_from']
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 输入正确的账号，返回用户名，否则返回none
        user = authenticate(username=username, password=password)
        # print "laiyuan=>>>>",request.META.get('HTTP_REFERER', '/blog')
        if user:
            print ("===登录用户名===", user)
            login(request, user)
            # 重定向到来源的url
            # return HttpResponseRedirect(request.session['login_from'])
            return redirect('/')
        else:
            return render(request, 'login.html', {'logs': '账号或密码错误！%s' % user})

    return render(request, 'login.html', {'logs': ' '})


def set_pwd(request):
    """修改密码"""
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method == "POST":
        oldpwd = request.POST.get("oldpwd")
        newpwd1 = request.POST.get("newpwd1")
        newpwd2 = request.POST.get("newpwd2")
        if not newpwd1 == newpwd2:
            info = "两次输入的密码不相同"
            return render(request, "set_pwd.html", {"logs": info})
        # 得到当前登录的用户，判断旧密码是不是和当前的密码一样
        username = request.user  # 打印的是当前登录的用户名
        user = UserInfo.objects.get(username=username)  # 查看用户
        ret = user.check_password(oldpwd)  # 检查密码是否正确
        if ret:
            user.set_password(newpwd1)  # 如果正确就给设置一个新密码
            user.save()  # 保存
            return redirect("/login/")
        else:
            info = "输入的旧密码不正确"
            return render(request, "set_pwd.html", {"logs": info})
    return render(request, "set_pwd.html")


def reg(request):
    """注册"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # password2 = request.POST.get("password2")
        email = request.POST.get("email")
        # first_name=request.POST.get("first_name")
        # last_name = request.POST.get("last_name")
        # if password1 != password2:
        #     return render(request, "blog/register.html", {'logs': '两次密码出入不一致'})
        name = UserInfo.objects.filter(username=username)
        # 如果用户存在，则name=1,不存在则name=0
        if name:
            return render(request, "register.html", {'message': '用户已存在%s' % len(name)})
        # else:
        # return render(request, "regist.html", {'logs': '用户bu存在%s' % len(name)})
        # 得到用户输入的用户名和密码创建一个新用户
        UserInfo.objects.create_user(username=username, password=password, email=email)

        # 注册成功后自动登录
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
    return render(request, "register.html")


def log_out(request):
    """注销"""
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")
