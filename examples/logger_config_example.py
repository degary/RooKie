"""
日志配置示例

展示如何在settings.py中配置不同的日志输出方式
"""

# 示例1: 只输出到控制台
LOGURU_CONFIG_CONSOLE_ONLY = {
    'console': {
        'enabled': True,
        'level': 'INFO',
    },
    'file': {
        'enabled': False,
    },
    'error_file': {
        'enabled': False,
    }
}

# 示例2: 只输出到文件
LOGURU_CONFIG_FILE_ONLY = {
    'console': {
        'enabled': False,
    },
    'file': {
        'enabled': True,
        'level': 'DEBUG',
        'path': 'logs/app.log',
    },
    'error_file': {
        'enabled': True,
        'level': 'ERROR', 
        'path': 'logs/error.log',
    }
}

# 示例3: 自定义路径和格式
LOGURU_CONFIG_CUSTOM = {
    'console': {
        'enabled': True,
        'level': 'WARNING',
        'format': "{time} | {level} | {message}"
    },
    'file': {
        'enabled': True,
        'level': 'INFO',
        'path': '/var/log/myapp/app.log',
        'rotation': '50 MB',
        'retention': '7 days',
    },
    'error_file': {
        'enabled': False,
    }
}