'''
Author: Abel icyheart1214@163.com
Date: 2022-05-27 15:21:07
LastEditors: Please set LastEditors
LastEditTime: 2023-06-19 14:07:17
Description: 
Copyright (c) 2022 by Abel icyheart1214@163.com, All Rights Reserved.
'''
import sys
import loguru
from .common import CONFIG

class MyLogger:
    __logger__ = None
    
    @classmethod
    @property
    def logger(cls):
        if not cls.__logger__:
            logger = loguru.logger
            logger.remove()
            logger.add(sys.stdout, level=CONFIG.log_level, enqueue=False)
            logger.add(
                'logs/LOG_{time:%Y-%m-%d}.log',
                enqueue=True, level='TRACE',
                colorize=True, rotation='00:00', retention=3
                )
            cls.__logger__ = logger
        return cls.__logger__

logger = MyLogger.logger
