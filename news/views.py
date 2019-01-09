# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from . import models
from concurrent.futures import ThreadPoolExecutor
import time
from pyquery import PyQuery

p = ThreadPoolExecutor(10)


def index(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 "
                      "Safari/537.36",
    }
    banana = []
    licai = []
    paper_title = []
    baidu_title = []
    car_title = []

    def get_pyquery(url):
        u"""通用请求"""
        pq = PyQuery(url=url, headers=headers, encoding='utf-8')
        return pq

    def hq_banana(res):
        """banana图"""
        pq = res.result()
        div = pq("#foucsBox ul.imgCon")
        # print div.html()
        li = div.find("li")
        # print li.html()
        for i in li.items():
            # print i.filter("li a").html()
            img = i.find("a").eq(0).find("img").attr("src")
            a = i.find(".imgTitle>a")
            href = a.attr("href")
            txt = a.html()
            if img:
                mydata = {
                    "txt": txt,
                    "href": href,
                    "img": img
                }
                # print txt, href
                # print img
                banana.append(mydata)

    def hx_money(res):
        """和讯理财"""
        pq = res.result()


        pass





    with ThreadPoolExecutor(10) as p:

        # 轮播图
        p.submit(get_pyquery, "http://world.huanqiu.com").add_done_callback(hq_banana)
        # 和讯理财
        p.submit(get_pyquery, "http://money.hexun.com").add_done_callback(hx_money)

    # time.sleep(1)

    return render(request, 'news/news.html', {"banana": banana})
