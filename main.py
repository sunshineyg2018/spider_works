# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------------
# Description:  
# Reference:
# Author: 
# Date:   2023/11/3
# -------------------------------------------------------------------------------
import logging

from utils import configure_logging
from weibo_spider.weibo import WeiBoFac

if __name__ == "__main__":
    configure_logging()
    WeiBoFac().main()

