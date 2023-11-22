# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------------
# Description:  知乎抓取
# Reference:
# Author: 
# Date:   2023/11/22
# -------------------------------------------------------------------------------
from DrissionPage import ChromiumPage
from utils import DisposeIni


class ZhiHuFac:
    def __init__(self):
        # 接管浏览器
        self.ini = dict(DisposeIni().get_items("zhihu"))
        page = ChromiumPage()

        page.get('')




