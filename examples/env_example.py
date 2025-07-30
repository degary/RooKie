"""
环境配置使用示例
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_env_config():
    """测试不同环境的日志配置"""

    # 测试开发环境
    print("=== 测试开发环境 ===")
    os.environ["DJANGO_SETTINGS_MODULE"] = "Rookie.settings.dev"

    # 重新导入模块以应用新配置
    if "utils.logger" in sys.modules:
        del sys.modules["utils.logger"]
    if "django.conf" in sys.modules:
        del sys.modules["django.conf"]

    from utils.logger import get_logger

    logger = get_logger()
    logger.info("开发环境日志测试", env="dev", level="INFO")
    logger.error("开发环境错误日志测试", env="dev", level="ERROR")

    # 测试测试环境
    print("\n=== 测试测试环境 ===")
    os.environ["DJANGO_SETTINGS_MODULE"] = "Rookie.settings.acc"

    # 重新导入模块以应用新配置
    if "utils.logger" in sys.modules:
        del sys.modules["utils.logger"]
    if "django.conf" in sys.modules:
        del sys.modules["django.conf"]

    from utils.logger import get_logger

    logger = get_logger()
    logger.info("测试环境日志测试", env="acc", level="INFO")
    logger.error("测试环境错误日志测试", env="acc", level="ERROR")

    print("\n环境配置测试完成！")
    print("查看 logs/ 目录下的不同环境日志文件：")

    logs_dir = project_root / "logs"
    if logs_dir.exists():
        for log_file in logs_dir.glob("*.log"):
            print(f"  - {log_file.name}")


if __name__ == "__main__":
    test_env_config()
