"""
生产环境配置
"""
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['example.com', 'www.example.com']

# 生产环境日志配置
LOGURU_CONFIG = {
    'console': {
        'enabled': False,  # 生产环境不输出到控制台
    },
    'file': {
        'enabled': True,
        'level': 'INFO',
        'path': '/var/log/rookie/app.log',  # 生产环境使用系统日志目录
        'rotation': '100 MB',
        'retention': '90 days',
        'compression': 'zip'
    },
    'error_file': {
        'enabled': True,
        'level': 'ERROR',
        'path': '/var/log/rookie/error.log',
        'rotation': '100 MB',
        'retention': '90 days',
        'compression': 'zip'
    }
}