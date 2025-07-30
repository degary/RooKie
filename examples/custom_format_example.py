"""
自定义日志格式示例
"""

# 在settings.py中可以这样配置：

# 示例1: 简化格式
SIMPLE_FORMAT_CONFIG = {
    "console": {
        "enabled": True,
        "level": "INFO",
        "format": "{time:HH:mm:ss} | {level} | {message}",
    }
}

# 示例2: JSON格式
JSON_FORMAT_CONFIG = {
    "file": {
        "enabled": True,
        "level": "INFO",
        "path": "logs/app.json",
        "format": '{"time": "{time}", "level": "{level}", "message": "{message}"}',
    }
}

# 示例3: 详细格式
DETAILED_FORMAT_CONFIG = {
    "console": {
        "enabled": True,
        "level": "DEBUG",
        "format": "[{time:YYYY-MM-DD HH:mm:ss.SSS}] {level} | {name}:{function}:{line} | {message}",
    }
}

# 示例4: 混合配置
MIXED_FORMAT_CONFIG = {
    "console": {
        "enabled": True,
        "level": "INFO",
        "format": "{time:HH:mm:ss} | {level} | {message}",  # 简化控制台
    },
    "file": {
        "enabled": True,
        "level": "DEBUG",
        "path": "logs/detailed.log",
        # 不指定format，使用默认格式（支持extra字段）
    },
}

print("请在 settings.py 中的 LOGURU_CONFIG 使用以上任一配置")
print("然后重启应用或调用 reset_logger() 来应用新格式")
