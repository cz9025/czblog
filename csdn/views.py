# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render
import requests


def index(request):
    u"""先分开写着，到时再合并再一个方法中"""
    py_title = []
    rfs_title = []
    function_title = []
    interface_title = []
    jmeter_title = []

    # 左边是栏目，右边是详情
    # 点击左边的栏目发起一个get请求，带一个参数过去
    # 参考博雅  关于我们的页面
    def get_index(url):
        response = requests.get(url)
        if response.status_code == 200:
            # print response.encoding
            return response.text

    def get_py(res, lists):
        res = res.result()
        html = etree.HTML(res)
        # 不包含特定元素的，这里排除为隐藏的元素；div的列表
        # 标题
        article = html.xpath('//*[@id="mainBox"]/main/div[2]/div[not(@style="display: none;")]/h4/a')
        # 摘要
        content = html.xpath('//*[@id="mainBox"]/main/div[2]/div[not(@style="display: none;")]/p/a')
        # 发布时间
        times=html.xpath('//*[@id="mainBox"]/main/div[2]/div[not(@style="display: none;")]/div/p[1]/span')
        # 阅读数
        cous=html.xpath('//*[@id="mainBox"]/main/div[2]/div[not(@style="display: none;")]/div/p[2]/span')
        # 评论数
        comens=html.xpath('//*[@id="mainBox"]/main/div[2]/div[not(@style="display: none;")]/div/p[3]/span')
        for i in range(len(article)):
            mycsdn = {}
            # 标题
            mycsdn['tt'] = article[i].xpath('./text()')[1].strip()
            # 链接地址
            mycsdn['urls'] = article[i].xpath('./@href')[0]
            # 摘要
            mycsdn['cont'] = content[i].xpath('./text()')[0].strip()
            # 发布时间
            mycsdn['times']=times[i].xpath('./text()')[0]
            # 阅读数
            mycsdn['cous']=cous[i].xpath('./text()')[0]
            # 评论数
            mycsdn['comens']=comens[i].xpath('./text()')[0]
            lists.append(mycsdn)


    def get_info(res):
        get_py(res, py_title)

    def get_rfs(res):
        get_py(res, rfs_title)

    def get_jmeter(res):
        get_py(res, jmeter_title)

    def get_function(res):
        get_py(res, function_title)

    def get_interface(res):
        get_py(res, interface_title)

    with ThreadPoolExecutor(10) as p:
        uri = "https://blog.csdn.net/cz9025/article/category/"
        # python
        p.submit(get_index, uri + '6810218').add_done_callback(get_info)
        # RF+SE
        p.submit(get_index, uri + '6810219').add_done_callback(get_rfs)
        # JMETER
        p.submit(get_index, uri + '6858016').add_done_callback(get_jmeter)
        # 接口测试
        p.submit(get_index, uri + '6966010').add_done_callback(get_interface)
        # 功能测试
        p.submit(get_index, uri + '6560600').add_done_callback(get_function)

    return render(request, 'csdn/csdn.html',
                  {'python': py_title, 'rfs': rfs_title, 'fun': function_title, 'intf': interface_title,
                   'jmeter': jmeter_title})
