# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render
from pyquery import PyQuery
import requests


def index(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 "
                      "Safari/537.36",
    }
    banana = []
    people = []
    baidu_net = []
    baidu_hot = []
    baidu_finance = []

    def get_pyquery(url, encode='UTF-8'):
        u"""通用请求"""
        response = requests.get(url, headers=headers)
        # print 'response=>>>>',response.content
        response.encoding = encode
        if response.status_code == 200:
            pq = PyQuery(response.text)
            return pq
        else:
            return 0

    def hq_banana(res):
        """环球 banana图"""
        pq = res.result()
        div = pq("div.focus-box ul")
        li = div.find("li")
        for i in li.items():
            img = i.find("a").eq(0).find("img").attr("src")
            a = i.find("a").eq(0)
            href = a.attr("href")
            txt = i.find("a").eq(0).find("img").attr("alt")
            if img:
                mydata = {
                    "txt": txt,
                    "href": href,
                    "img": img
                }
                # print mydata
                banana.append(mydata)

    def hx_money(res):
        """人民网"""
        pq = res.result()
        # print "pq=>>>>>",pq
        hdnews = pq('.headingNews_box .headingNews:first').find(".hdNews")
        # print "hdnews=>>>>",hdnews
        for news in hdnews.items():
            a = news.find("strong a")
            if a:
                a_title = a.html()
                a_href = "http://house.people.com.cn" + a.attr("href")
                gray = news.find("p a").html()
                mydata = {
                    "a_title": a_title,
                    "a_href": a_href,
                    "gray": gray
                }
                people.append(mydata)

    def bd_hot_news(res):
        """百度新闻  热点要闻"""
        pq = res.result()
        top = pq("#pane-news>div>ul").find("li")
        bot = pq("#pane-news>ul:first").find("li")
        strs = top + bot
        for i in strs.items():
            mydata = {
                "a_title": i.find("a").html(),
                "a_href": i.find("a").attr("href")
            }
            baidu_hot.append(mydata)

    def bd_net_news(res):
        """百度新闻  互联网新闻"""
        pq = res.result()
        titles = pq("#internet_news>ul").find("li")
        for title in titles.items():
            a_title = title.find("a").html()
            a_href = title.find("a").attr("href")
            mydata = {
                "a_title": a_title,
                "a_href": a_href
            }
            baidu_net.append(mydata)

    def bd_finance_news(res):
        """百度新闻  财经新闻"""
        pq = res.result()
        titles = pq("#col_focus .middle-focus-news").find("li")
        for title in titles.items():
            a_title = title.find("a").html()
            a_href = title.find("a").attr("href")
            mydata = {
                "a_title": a_title,
                "a_href": a_href
            }
            baidu_finance.append(mydata)

    with ThreadPoolExecutor(10) as p:
        # 编码为UTF-8的可以不写，其余都要写下

        # 轮播图
        p.submit(get_pyquery, "http://world.huanqiu.com").add_done_callback(hq_banana)
        # 人民网  房产
        p.submit(get_pyquery, "http://house.people.com.cn", 'GB2312').add_done_callback(hx_money)
        # 百度热点要闻
        p.submit(get_pyquery, "https://news.baidu.com").add_done_callback(bd_hot_news)
        # 百度互联网新闻
        p.submit(get_pyquery, "https://news.baidu.com/tech").add_done_callback(bd_net_news)
        # 百度财经新闻
        p.submit(get_pyquery, "https://news.baidu.com/finance").add_done_callback(bd_finance_news)

    return render(request, 'news/news.html', locals())
