# -------------------------------------------------------------------------------
# Description:  微博
# Reference:
# Author: 
# Date:   2023/11/1
# -------------------------------------------------------------------------------
import logging

logger = logging.getLogger()
file_handler = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

