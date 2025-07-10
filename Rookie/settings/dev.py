"""
开发环境配置
"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']  # 开发环境允许所有主机

# CSRF 可信来源配置（支持ngrok等内网穿透工具）
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://*.ngrok.io',
    'https://*.ngrok-free.app',
    'https://*.ngrok.app',
]

# 开发环境日志配置
LOGURU_CONFIG = {
    'console': {
        'enabled': True,
        'level': 'INFO',  # 控制台显示INFO及以上级别
    },
    'file': {
        'enabled': True,  # 开发环境启用文件日志
        'level': 'DEBUG',
        'path': BASE_DIR / 'logs' / 'dev.log',
        'rotation': '10 MB',
        'retention': '7 days',
    },
    'error_file': {
        'enabled': True,  # 启用错误日志
        'level': 'ERROR',
        'path': BASE_DIR / 'logs' / 'dev_error.log',
        'rotation': '10 MB',
        'retention': '7 days',
    }
}

# 禁用Django原生日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
}