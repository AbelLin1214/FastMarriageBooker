<!--
 * @Author: Abel
 * @Date: 2023-06-19 13:27:10
 * @LastEditTime: 2023-06-19 14:11:51
-->
## `婚姻登记网上预约系统`自动预约程序

### 使用方法

首先克隆仓库，随后按照以下步骤

#### 步骤1

本项目基于``ttshitu``进行验证码识别，需要先注册账号并至少充值1元，[点我注册](http://ttshitu.com)

#### 步骤2

本项目使用``Server酱``进行通知，请访问[Server酱](https://sct.ftqq.com)，按照相应步骤获取Send Key

#### 步骤3

安装依赖，建议使用``conda``创建虚拟环境后安装

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 运行

完成以上步骤后，请在config.yaml中填写相应信息，随后执行``python -m marriage_booker``

### 请注意
1. 仅限**广东省**内预约
2. 本人仅测试了深圳，其余地区未经测试，理论可用
3. 本项目仅供学习和参考使用，请不要用于商业、违法途径，本人不对此源码造成的违法负责！