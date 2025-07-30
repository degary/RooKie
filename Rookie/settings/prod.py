"""
生产环境配置
"""
import os

from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# 静态文件配置
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# PostgreSQL数据库配置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "rookie"),
        "USER": os.getenv("DB_USER", "rookie"),
        "PASSWORD": os.getenv("DB_PASSWORD", "rookie123"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# CSRF 可信来源配置（支持ngrok等内网穿透工具）
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://*.ngrok.io",
    "https://*.ngrok-free.app",
    "https://*.ngrok.app",
]

# 生产环境日志配置
LOGURU_CONFIG = {
    "console": {"enabled": True, "level": "DEBUG"},
    "file": {
        "enabled": True,
        "level": "INFO",
        "path": BASE_DIR / "logs" / "app.log",
        "rotation": "100 MB",
        "retention": "90 days",
        "compression": "zip",
    },
    "error_file": {
        "enabled": True,
        "level": "ERROR",
        "path": BASE_DIR / "logs" / "error.log",
        "rotation": "100 MB",
        "retention": "90 days",
        "compression": "zip",
    },
}

# 启用Django调试日志
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
