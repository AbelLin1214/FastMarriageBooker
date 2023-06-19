'''
Author: Abel
Date: 2023-06-19 09:42:00
LastEditTime: 2023-06-19 11:45:12
'''
import io
import base64
from PIL import Image, ImageChops, ImageSequence

class ImageTool:
    '''Image操作工具类'''

    def from_bytes(data: bytes):
        '''从bytes数据创建Image对象'''
        return Image.open(io.BytesIO(data))
    
    def to_base64(img: Image.Image):
        '''将Image对象转换为base64编码的字节流'''
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        img_bytes = buffer.getvalue()
        b64_bytes = base64.b64encode(img_bytes)
        return b64_bytes

    def to_base64_str(img: Image.Image):
        '''将Image对象转换为base64编码字符串'''
        b64_bytes = ImageTool.to_base64(img)
        return b64_bytes.decode('ascii')
    
    def from_base64_str(b64_str: str):
        '''从base64编码字符串创建Image对象'''
        b64_bytes = b64_str.encode('ascii')
        img_bytes = base64.b64decode(b64_bytes)
        return ImageTool.from_bytes(img_bytes)

    def multiply_gif(img: Image.Image):
        '''
        将多层图像的像素值相乘以得到最终的图像

        实现Photoshop中的"正片叠底Multiply blending mode"效果
        '''
        # 获取所有帧
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]

        # 初始化结果图像为第一帧
        result = frames[0].convert('RGB')

        # 遍历剩余的帧，将像素值相乘
        for frame in frames[1:]:
            frame_rgb = frame.convert('RGB')
            result = ImageChops.multiply(result, frame_rgb)
        return result
