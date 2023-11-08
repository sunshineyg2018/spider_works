# -------------------------------------------------------------------------------
# Description:  
# Reference:
# Author: 
# Date:   2023/11/1
# -------------------------------------------------------------------------------
import random
import time

from utils import DisposeIni
import requests
import os

from weibo_spider import logger


class WeiBoFac:
    def __init__(self, input_cookie=None):
        self.wb_text = []
        self.ini = dict(DisposeIni().get_items("weibo"))
        try:
            self.frequency_start_time,self.frequency_end_time = self.ini["time_sleep"].split(",")
            self.frequency_start_time = int(self.frequency_start_time)
            self.frequency_end_time = int(self.frequency_end_time)
        except ValueError:
            self.frequency_start_time = 1
            self.frequency_end_time = 5

        # Todo 验证爬取名单 未写
        self.spider_list = eval(self.ini["spider_list"])
        if input_cookie is None:
            input_cookie = self.ini.get("cookie")
            if input_cookie == "":
                raise ValueError("请传入正确的cookie")

        self.headers = {
            'authority': 'weibo.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/118.0.0.0 Safari/537.36',
            'Cookie': input_cookie
        }

    def __get_account_info(self,uid):
        """获取账户信息"""
        try:
            url = "https://weibo.com/ajax/profile/info?uid={}"
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                res_json = res.json()
                return res_json["data"]["user"]["screen_name"]
            return ""
        except Exception as e:
            logger.error(e.__traceback__)
            return ""

    def __get_weibo_article(self, uid):
        """获取微博作者所发所有信息"""
        def get_article_data(page):
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={uid}&page={page}&feature=0"
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                res_json = res.json()
                # todo 判断是不是正确的返回 未写
                # short_text:短文本
                # long_text_mblogid_list:长文本
                long_text_mblogid_list = []
                short_text_list = []
                for obj in res_json["data"]["list"]:
                    is_long_text = obj["isLongText"]
                    if not is_long_text:
                        short_text_list.append(obj["text_raw"])
                    else:
                        long_text_mblogid_list.append(obj["mblogid"])
                return {
                    "next_page_since_id":res_json["data"]["since_id"],
                    "long_text_mblogid_list":long_text_mblogid_list,
                    "short_text_list":short_text_list,
                }

        # todo 验证抓取的一种方式

        # 获取按页数爬取的参数
        page_num = self.ini.get("page_num","")
        if page_num != "" and isinstance(page_num,int):
            for n in range(page_num):
                n += 1
                logger.info(f"抓取任务运行成功...当前抓取页面{n}")
                article_data_obj = get_article_data(n)
                self.__analyze_struct_text(article_data_obj)
                time.sleep(random.randint(self.frequency_start_time,self.frequency_end_time))

    def __analyze_struct_text(self,article_data_obj):
        """解析文本结构体"""
        long_text_list = article_data_obj.get("long_text_mblogid_list")
        if long_text_list is not None:
            for n in long_text_list:
                url = f"https://weibo.com/ajax/statuses/longtext?id={n}"
                res = requests.get(url, headers=self.headers)
                if res.status_code == 200:
                    res_json = res.json()
                    if res_json["data"] == {}:
                        continue
                    else:
                        self.wb_text.append(res_json["data"]["longTextContent"])
                time.sleep(random.randint(self.frequency_start_time,self.frequency_end_time))

        short_text_list = article_data_obj.get("short_text_list")
        if short_text_list is not None:
            for n in short_text_list:
                self.wb_text.append(n)

    def output(self):
        # 获取输出方式
        output_type = self.ini.get("output_type")
        output_path = self.ini.get("output_path")
        self.spider_list = self.spider_list if isinstance(self.spider_list,list) else [self.spider_list]
        if output_path == "":
            output_path = os.getcwd()

        if output_type == "":
            raise ValueError("至少选择一个输出方式")
        else:
            output_type = eval(output_type)
            # 多种输出方式
            if isinstance(output_type,list):
                for uid in self.spider_list:
                    nike_name = self.__get_account_info(uid)
                    if nike_name != "":
                        logger.info(f"抓取任务运行成功...当前抓取{nike_name}")
                        self.__get_weibo_article(uid)
                        if "txt" in output_type:
                            for n in self.wb_text:
                                with open(os.path.join(output_path,f"{nike_name}.txt"),"a") as f:
                                    f.write(n)
                                    f.write("\n")
                    else:
                        raise ValueError("请确认爬取账户名单的id是否正确")
                    # 清空
                    self.wb_text.clear()

            elif isinstance(output_type,str):
                pass
            else:
                raise ValueError("请确认参数类型,目前只支持list和str")





