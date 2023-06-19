'''
Author: Abel
Date: 2023-06-19 09:58:16
LastEditTime: 2023-06-19 11:33:37
'''
import yaml
from pathlib import Path
from models import Config

def load_config(path: str):
    '''加载配置文件'''
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'配置文件不存在: {path}')
    data = p.read_bytes()
    config = yaml.safe_load(data)
    return Config.parse_obj(config)

CONFIG = load_config('config.yaml')
