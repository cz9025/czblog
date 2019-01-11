# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from . import models
from concurrent.futures import ThreadPoolExecutor
import time
from pyquery import PyQuery
import requests

p = ThreadPoolExecutor(10)


def index(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 "
                      "Safari/537.36",
    }
    banana = []
    people = []
    paper_title = []
    baidu = []
    car_title = []

    def get_pyquery(url):
        u"""通用请求  , encoding='utf-8'"""
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pq = PyQuery(response.content)
            return pq
        else:
            return 0

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
        """人民网"""
        pq = res.result()
        # pq = PyQuery(div)

        headingNews = pq('.headingNews_box .headingNews:first').find(".hdNews")
        for news in headingNews.items():
            a = news.find("strong a")
            if a:
                a_title = a.text()
                a_href = "http://house.people.com.cn" + a.attr("href")
                gray = news.find("p a").text()

                mydata = {
                    "a_title": a_title,
                    "a_href": a_href,
                    "gray": gray
                }
                print mydata
                people.append(mydata)

    def bd_news(res):
        """百度新闻"""
        pq = res.result()
        top = pq("#pane-news>div>ul").find("li")
        bot = pq("#pane-news>ul:first").find("li")
        strs = top + bot
        for i in strs.items():
            mydata = {
                "a_title": i.find("a").html(),
                "a_href": i.find("a").attr("href")
            }
            baidu.append(mydata)

    with ThreadPoolExecutor(10) as p:
        # 轮播图
        p.submit(get_pyquery, "http://world.huanqiu.com").add_done_callback(hq_banana)
        # 人民网  房产
        p.submit(get_pyquery, "http://house.people.com.cn").add_done_callback(hx_money)
        # 百度新闻
        p.submit(get_pyquery, "https://news.baidu.com").add_done_callback(bd_news)

    return render(request, 'news/news.html', {"banana": banana, "people": people, "baidu": baidu})
