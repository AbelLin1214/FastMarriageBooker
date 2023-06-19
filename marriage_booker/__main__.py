'''
Author: Abel
Date: 2023-06-19 14:08:21
LastEditTime: 2023-06-19 14:08:21
'''
import asyncio
from .core import AutoRegister

if __name__ == '__main__':
    r = AutoRegister()
    asyncio.run(r.run())
