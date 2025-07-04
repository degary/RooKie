"""
测试环境配置
"""
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['test.example.com', 'acc.example.com']

# 测试环境日志配置
LOGURU_CONFIG = {
    'console': {
        'enabled': False,  # 测试环境不输出到控制台
    },
    'file': {
        'enabled': True,
        'level': 'INFO',
        'path': BASE_DIR / 'logs' / 'acc.log',
        'rotation': '50 MB',
        'retention': '30 days',
        'compression': 'zip'
    },
    'error_file': {
        'enabled': True,
        'level': 'ERROR',
        'path': BASE_DIR / 'logs' / 'acc_error.log',
        'rotation': '50 MB',
        'retention': '30 days',
        'compression': 'zip'
    }
}