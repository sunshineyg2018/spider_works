# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------------
# Description:  知乎文章抓取
# Reference:
# Author: 
# Date:   2023/11/22
# -------------------------------------------------------------------------------
import time

from DrissionPage import WebPage
from utils import DisposeIni
import os
from loguru import logger


class ZhiHuFac:
    def __init__(self):
        # 接管浏览器
        self.page = WebPage()
        self.url_template = "https://www.zhihu.com/people/{}/posts"
        self.ini = dict(DisposeIni().get_items("zhihu"))
        self.output_type = self.ini.get("output_type")
        self.output_path = self.ini.get("output_path")
        if self.output_path == "":
            self.output_path = os.getcwd()
        self.nike_name = ""
        try:
            self.frequency_start_time,self.frequency_end_time = self.ini["time_sleep"].split(",")
            self.frequency_start_time = int(self.frequency_start_time)
            self.frequency_end_time = int(self.frequency_end_time)
        except ValueError:
            self.frequency_start_time = 1
            self.frequency_end_time = 5
        self.spider_list = eval(self.ini["spider_account_list"])

    def get_zhihu_html_article_data(self):
        js = 'JSON.parse(document.getElementById("js-initialData").textContent)'
        article_info = self.page.run_js(js, as_expr=True)["initialState"]["entities"]["articles"]
        return article_info

    def analytic_data(self,article_info):
        for key in article_info:
            article_data = article_info[key]
            # 标题
            title = article_data["title"]
            # 评论数
            comment_count = article_data["commentCount"]
            # 喜欢数
            like = article_data["voteupCount"]
            # 文章url
            url = article_data["url"]
            # 验证是否能通过requests 获取到文章内容

    def main(self):
        self.page.change_mode("d",go=False,copy_cookies=False)

        for account in self.spider_list:
            last_num = 0
            self.page.get(self.url_template.format(account))
            loading_status = self.page.wait.load_complete()
            if loading_status:
                article_info = self.get_zhihu_html_article_data()
                ele1 = self.page.ele('.Pagination')
                button_list = ele1.eles('tag:button')[-2]
                try:
                    last_num = int(button_list.text) + 1
                except ValueError:
                    raise ValueError("获取最大页失败,请确认账号队列")

            for page in range(2,last_num):
                self.url_template = "https://www.zhihu.com/people/{}/posts?page={}".format(
                    account,
                    page
                )
                self.page.get(self.url_template.format(account))
                article_info = self.get_zhihu_html_article_data()















