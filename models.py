'''
Author: Abel
Date: 2023-06-19 09:58:21
LastEditTime: 2023-06-19 13:26:39
'''
from typing import Literal
from pydantic import BaseModel, Field
import datetime

class PersonalDetail(BaseModel):
    '''个人信息'''
    name: str = Field(..., min_length=2, title='姓名')
    id: str = Field(..., min_length=18, max_length=18, title='身份证号')
    phone: str = Field(..., min_length=11, max_length=11, title='手机号')
    # 学历,请从以下选项输入
    # 文盲或半文盲、小学、初中、高中、中专、大专、大学、硕士研究生、博士研究生
    education: Literal[
        '文盲或半文盲',
        '小学',
        '初中',
        '高中',
        '中专',
        '大专',
        '大学',
        '硕士研究生',
        '博士研究生'
    ] = Field(..., title='学历')

    occupation: Literal[
        '国家机关，党群组织，企事业单位',
        '商业、服务业人员',
        '生产、运输设备操作人员及有关人员',
        '办事人员和有关人员',
        '农、林、牧、渔、水利业生产人员',
        '军人',
        '专业技术人员',
        '无业人员',
        '其他从业人员'
    ] = Field(..., title='职业')

class TTShiTu(BaseModel):
    '''TT识图配置'''
    username: str = Field(..., title='用户名')
    password: str = Field(..., title='密码')
    type_id: int = Field(..., title='识别类型ID')

class Config(BaseModel):
    '''全局配置'''
    male: PersonalDetail = Field(..., title='男方信息')
    female: PersonalDetail = Field(..., title='女方信息')
    ft_send_key: str = Field(..., title='方糖SendKey')
    log_level: Literal[
        'TRACE', 'DEBUG', 'INFO', 'SUCCESS',
        'WARNING', 'ERROR', 'CRITICAL'] = Field('INFO', title='日志等级')
    city: str = Field(..., title='城市')
    areas: list[str] = Field(..., title='区｜县')
    date: datetime.date = Field(..., title='日期')
    ttshitu: TTShiTu = Field(..., title='TT识图配置')
    headless: bool = Field(..., title='是否无头模式')
