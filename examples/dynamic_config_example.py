"""
动态更改日志配置示例
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logger import get_logger, reset_logger


def demo_dynamic_config():
    # 使用默认配置
    logger = get_logger()
    logger.info("使用默认配置", userId=123)

    # 动态修改配置
    from django.conf import settings

    # 修改为简化格式
    settings.LOGURU_CONFIG = {
        "console": {
            "enabled": True,
            "level": "INFO",
            "format": "{time:HH:mm:ss} | {level} | {message}",
        },
        "file": {"enabled": False},
        "error_file": {"enabled": False},
    }

    # 重置logger应用新配置
    reset_logger()
    logger = get_logger()
    logger.info("使用新配置", userId=456)


if __name__ == "__main__":
    demo_dynamic_config()
