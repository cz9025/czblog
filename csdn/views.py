# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render
from django.http import JsonResponse
from lxml import etree
import requests
import re
import time

p = ThreadPoolExecutor(30)


def index(request):
    uri = "https://blog.csdn.net/cz9025/category_"
    # 栏目内容
    column_title = []
    # 左侧的分类标题
    left_title = []

    def get_index(url):
        response = requests.get(url)
        if response.status_code == 200:
            # print response.encoding
            return response.text

    def get_py(res):
        res = res.result()
        html = etree.HTML(res)
        # 不包含特定元素的，这里排除为隐藏的元素；div的列表
        # 标题
        article = html.xpath('//*[@id="column"]/ul/li//div[1]/h2')
        # 链接地址
        aurl = html.xpath('//*[@id="column"]/ul/li/a')
        # 摘要
        content = html.xpath('//*[@id="column"]/ul/li//div[2]')
        # 发布时间
        times = html.xpath('//*[@id="column"]/ul/li//div[3]/span[1]')
        # 阅读数
        cous = html.xpath('//*[@id="column"]/ul/li//div[3]/span[2]')
        # 评论数
        comens = html.xpath('//*[@id="column"]/ul/li//div[3]/span[3]')
        for i in range(len(article)):
            mycsdn = {}
            # 标题
            mycsdn["tt"] = article[i].xpath('./text()')[0].strip()
            # 链接地址
            mycsdn["urls"] = aurl[i].xpath('./@href')[0]
            # 摘要
            mycsdn["cont"] = content[i].xpath('./text()')[0].strip()
            # 发布时间
            mycsdn["times"] = times[i].xpath('./text()')[0]
            # 阅读数
            mycsdn["cous"] = cous[i].xpath('./text()')[0]
            # 评论数
            mycsdn["comens"] = comens[i].xpath('./text()')[0]
            column_title.append(mycsdn)
        # print "column_title=>>>>>",column_title
        # print "article=>>>>", article

    if request.GET:
        # 获取点击的那个分类编号
        dataurl = request.GET.get('dataurl')
        # print "dataurl=>>>>",dataurl
        # 根据编号再次发起请求，获得分类下的内容
        p.submit(get_index, uri + str(dataurl) + ".html").add_done_callback(get_py)

        time.sleep(1)
        # 如果列表还是为空的话，再休眠几秒钟
        if not column_title:
            time.sleep(3)

        column = dict()
        column["result"] = 10000
        column["msg"] = column_title
        # 默认只能传递字典类型，如果要传递非字典类型需要设置一下safe关键字参数。
        return JsonResponse(column)

    # 分类 进来的时候加载一次
    def get_lanmu(res):
        res = res.result()
        html = etree.HTML(res)
        a_lan = html.xpath('//*[@id="asideCategory"]/div/ul/li/a')
        default_url = a_lan[0].xpath('./@href')[0]
        # print "default_url===>>>>>>>", default_url
        for span in a_lan:
            mycsdn = {}
            a_title = span.xpath('./span[1]/span/text()')[0]
            mycsdn['biaoti'] = a_title
            mycsdn['aurl'] = re.findall(r'\d+', span.xpath('./@href')[0])[-1]
            # print re.findall(r'\d+', span.xpath('./@href')[0])[-1]
            pian = span.xpath('./span[2]/text()')
            if pian:
                mycsdn['cout'] = pian[0]
            else:
                mycsdn['cout'] = u"0篇"

            # print a_title
            left_title.append(mycsdn)
        # print biao_ti[0]['aurl']
        #  默认的 展示第一个栏目的
        p.submit(get_index, default_url).add_done_callback(get_py)

    # 左侧的栏目
    p.submit(get_index, "https://blog.csdn.net/cz9025/").add_done_callback(get_lanmu)

    time.sleep(1)
    # 如果列表还是为空的话，再休眠几秒钟
    if not left_title:
        time.sleep(3)

    return render(request, 'csdn/csdn.html', {'python': column_title, 'bti': left_title})
