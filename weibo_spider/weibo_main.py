# -------------------------------------------------------------------------------
# Description:  
# Reference:
# Author: 
# Date:   2023/11/1
# -------------------------------------------------------------------------------
from utils import DisposeIni
import requests


class WeiBoFac:
    def __init__(self, input_cookie=None):
        self.ini = dict(DisposeIni().get_items("weibo"))
        # Todo 验证必须名单 未写
        self.spider_list = eval(self.ini["spider_list"])
        if input_cookie is None:
            input_cookie = self.ini.get("cookie")
            # Todo 验证是否添加cookie 未写

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

    def __get_weibo_article(self, uid):
        """获取微博作者所发所有信息"""
        def get_article(page):
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={uid}&page={page}&feature=0"
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                res_json = res.json()
                # todo 判断是不是正确的返回 未写
                long_text_mblogid_list = []
                for mblogid in res_json["data"]["list"]:
                    # 排除视频,后期增加
                    if mblogid.get("page_info") is not None:
                        long_text_mblogid_list.append(mblogid["mblogid"])
                return {
                    "next_page_since_id":res_json["data"]["since_id"],
                    "long_text_mblogid_list":long_text_mblogid_list
                }
        page_num = self.ini.get("page_num", -1)
        if self.ini.get("page_num") != -1:
            for n in page_num:
                n += 1
                get_article(n)

    def output_long_text(self):
        """输出长文本"""
        pass

    def output(self):
        pass


if __name__ == "__main__":
    spider_obj = WeiBoFac()
