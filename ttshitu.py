'''
Author: Abel
Date: 2023-06-19 12:44:52
LastEditTime: 2023-06-19 12:56:24
'''
from httpx import AsyncClient
from pydantic import BaseModel

class TTError(Exception): ...

class TTShiTuData(BaseModel):
    '''打码平台响应数据'''
    result: str
    id: str

class TTShiTuResponse(BaseModel):
    '''打码平台响应'''
    success: bool
    code: str
    message: str
    data: TTShiTuData|str

class TTShiTu:
    '''打码平台'''
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = AsyncClient(
            base_url='http://api.ttshitu.com',
            timeout=10
            )

    async def predict(self, img_b64: str, typeid: int):
        '''打码，详见开发文档
        http://www.ttshitu.com/docs/python.html#pageTitle
        '''
        data = {
            "username": self.username,
            "password": self.password,
            "typeid": typeid,
            "image": img_b64
            }
        resp = await self.client.post("/predict", json=data)
        result = TTShiTuResponse.parse_obj(resp.json())
        if result.success:
            return result.data
        raise TTError(result.message)
    
    async def report_error(self, id: str):
        '''反馈打码错误'''
        data = {'id': id}
        resp = await self.client.post("/reporterror.json", json=data)
        result = TTShiTuResponse.parse_obj(resp.json())
        if result.success:
            return result.data
        raise TTError(result.message)
