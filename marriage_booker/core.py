'''
Author: Abel icyheart1214@163.com
Date: 2022-08-02 14:05:17
LastEditors: Please set LastEditors
LastEditTime: 2023-06-22 01:12:51
Description: 
Copyright (c) 2022 by Abel icyheart1214@163.com, All Rights Reserved.
'''
import re
import asyncio
from playwright.async_api._generated import Response, ElementHandle
from playwright.async_api import async_playwright
from httpx import AsyncClient
from .logger import logger
from .common import CONFIG
from .utils import ImageTool
from .ttshitu import TTShiTu, TTShiTuData

class AutoRegister:
    def __init__(self):
        self.url = 'https://www.gdhy.gov.cn/'
        self.client = AsyncClient()
        self.code = ''
        self.i = 0
        self.date = CONFIG.date.strftime('%Y-%m-%d')
        self.selected_county = '|'.join(CONFIG.areas)
        self.ttshitu = TTShiTu(
            CONFIG.ttshitu.username, CONFIG.ttshitu.password
        )
        self.__predict_data: TTShiTuData = None
    
    async def send_notice(self, params: dict):
        url = 'https://sctapi.ftqq.com/{}.send'
        url = url.format(CONFIG.ft_send_key)
        await self.client.get(url, params=params)
    
    async def parse_code(self, img_data: bytes):
        '''打码，详见开发文档
        http://www.ttshitu.com/docs/python.html#pageTitle'''
        # 加载gif
        gif = ImageTool.from_bytes(img_data)
        # 将gif以正片叠底方式合并
        multiply_img = ImageTool.multiply_gif(gif)
        # 转base64字符串
        b64 = ImageTool.to_base64_str(multiply_img)
        self.__predict_data = await self.ttshitu.predict(b64, CONFIG.ttshitu.type_id)
        return self.__predict_data.result

    async def on_response(self, response: Response):
        try:
            if 'https://www.gdhy.gov.cn/common.do?do=getCaptchaImg'\
                in response.url and response.status == 200:
                data = await response.body()
                if len(data) > 1000:
                    self.code = await self.parse_code(data)
                    logger.info(f'检测到验证码，识别结果为{self.code}')
        except:
            ...

    async def run(self):
        async with async_playwright() as playwright:
            self.browser = await playwright.chromium.launch(
                headless=CONFIG.headless,
                channel='chrome',
                args=['--disable-blink-features=AutomationControlled']
            )
            await self.run_forever()

    async def get_captcha_element_from_script(self):
        '''从HTML script标签中获取验证码输入框与提交按钮'''
        logger.info('正在尝试从HTML script标签中获取验证码输入框与提交按钮')
        js = await self.page.query_selector('//script[contains(text(), "captcha")]')
        js_script = await js.inner_text()
        p = r'function (\w{20,})?\(.+?name\=(\w+).*'
        ret = re.search(p, js_script, re.DOTALL)
        if ret:
            captcha_input = await self.page.wait_for_selector(
                f'//input[@name="{ret[2]}"]'
                )
            btn = await self.page.wait_for_selector(
                f'//input[@onclick="{ret[1]}();"]'
                )
            return captcha_input, btn

        return None, None
    
    async def input_code(self):
        '''输入验证码'''
        while True:
            try:
                submit_btn = await self.page.query_selector('//input[@class="btn_1"]')
                captcha_input = await self.page.query_selector('//input[@class="capcha_input"]')
                if not captcha_input:
                    captcha_input, submit_btn = await self.get_captcha_element_from_script()
                    if not captcha_input:
                        logger.info('未检测到验证码输入框，跳过')
                        break
                await captcha_input.fill(self.code, timeout=5000)
                async with self.page.expect_navigation(timeout=3000):
                    await submit_btn.click(timeout=3000)
                await self.page.wait_for_load_state('networkidle')
                break
            except Exception as e:
                logger.warning(f'{e.__class__.__name__}: {e}')
                # 反馈打码错误
                await self.ttshitu.report_error(self.__predict_data.id)
                logger.debug('成功反馈打码错误')
                await asyncio.sleep(1)
                continue
    
    async def select_info(self):
        '''
        前置信息选择

        需要选择户籍所在省、市、街道，填写户籍地址

        实测`并不校验户籍地址`，只要填写了就可以

        这里选择深圳市福田区福田街道办事处

        户籍地址填写深圳市
        '''
        fmt = '//select[@id="{}"]'
        selexes = [
            ('area_citynan', '深圳市'),
            ('area_citynv', '深圳市'),
            ('area_countynan', '福田区'),
            ('area_countynv', '福田区'),
            ('area_townnan', '福田街道办事处'),
            ('area_townnv', '福田街道办事处'),
        ]
        for _id, v in selexes:
            selex = fmt.format(_id)
            try:
                # await self.page.click(selex)
                await self.page.select_option(selex, label=v, timeout=3000)
            except Exception as e:
                logger.warning(f'{e.__class__.__name__}: {e}')
        await self.page.fill('//input[@id="fjdnan"]', CONFIG.city)
        await self.page.fill('//input[@id="fjdnv"]', CONFIG.city)
        try:
            async with self.page.expect_navigation(timeout=3000):
                await self.page.click('//input[@class="btn_1"]')
            await self.page.wait_for_load_state('networkidle')
        except Exception as e:
            logger.warning(f'{e.__class__.__name__}: {e}')
    
    async def register(self, e: ElementHandle, name: str):
        select_btn = await e.query_selector('//input[@name="djjg"]')
        await select_btn.click()
        await self.page.wait_for_timeout(1000)
        t_e = await self.page.query_selector('//input[@name="yysj"]/../../td[4]')
        t = await t_e.inner_text()
        await self.page.click('//input[@name="yysj"]')
        async with self.page.expect_navigation(timeout=3000):
            await self.page.click('//input[@class="btn_1"]')
        await self.page.wait_for_load_state('networkidle')
        await self.page.fill('//input[@name="xmnan"]', CONFIG.male.name)
        await self.page.fill('//input[@name="xmnv"]', CONFIG.female.name)
        await self.page.fill('//input[@name="sfzjhmnan"]', CONFIG.male.id)
        await self.page.fill('//input[@name="sfzjhmnv"]', CONFIG.female.id)
        await self.page.select_option('//select[@name="whcdnan"]', label=CONFIG.male.education)
        await self.page.select_option('//select[@name="whcdnv"]', label=CONFIG.female.education)
        await self.page.select_option('//select[@name="zynan"]', label=CONFIG.male.occupation)
        await self.page.select_option('//select[@name="zynv"]', label=CONFIG.female.occupation)
        await self.page.fill('//input[@name="lxdhnan"]', CONFIG.male.phone)
        await self.page.fill('//input[@name="lxdhnv"]', CONFIG.female.phone)
        await self.input_code()
        params = {
            'title': f'已预约{name} {self.date} {t} ',
            'desp': f'已预约{name} {self.date} {t} '
        }
        await self.send_notice(params)
    
    @logger.catch
    async def auto_refresh(self):
        await self.page.fill('//input[@id="yyrq"]', self.date)
        await self.page.select_option('//select[@name="blcs"]', label=CONFIG.city + '市')
        while True:
            refresh_btn = await self.page.query_selector('//a[@class="querybtn"]')
            if refresh_btn:
                await refresh_btn.click()
                await self.page.wait_for_load_state('networkidle')
                self.i += 1
                elements = await self.page.query_selector_all('//input[@type="radio"]/../..')
                for e in elements:
                    left_element = await e.query_selector('//td[@style]')
                    left_value = await left_element.inner_text()
                    name_element = await e.query_selector('//td[@id]')
                    name = await name_element.inner_text()
                    if int(left_value) > 0:
                        logger.success(f'{name} 当前可预约！可预约量为：{left_value}')
                        params = {
                            'title': f'{name} 婚姻登记有号啦！！！！ 剩余: {left_value}',
                            'desp': f'民政局：{name}\n剩余预约号：{left_value}\n冲冲冲！'
                        }
                        await self.send_notice(params)
                        if re.search(self.selected_county, name):
                            await self.register(e, name)
                            input('按回车键退出')
                    logger.trace(f'{name} 当前剩余预约量为：{left_value}')
                logger.info(f'第{self.i}次刷新已执行，没有检测到预约号，3秒后刷新')
                await asyncio.sleep(3)
            else:
                logger.warning('会话已过期，重新运行')
                break

    async def run_forever(self):
        while True:
            self.context = await self.browser.new_context()
            await self.context.add_init_script(path='statics/stealth.min.js')
            self.page = await self.context.new_page()
            self.page.on('response', self.on_response)
            # 自动处理弹窗
            # 需要注意，这样会导致页面上的alert无法弹出
            # 例如身份证号码错误的弹窗
            self.page.on('dialog', lambda dialog: dialog.accept())
            await self.page.goto(self.url)
            await self.page.wait_for_load_state('networkidle')
            await self.input_code()
            async with self.page.expect_navigation(timeout=3000):
                await self.page.click('//img[@alt="预约结婚"]', timeout=3000)
            await self.page.wait_for_load_state('networkidle')
            await self.select_info()
            await self.auto_refresh()
            await self.page.close()
            await self.context.close()
