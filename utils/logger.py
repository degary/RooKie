from loguru import logger
from pathlib import Path
import sys

# 初始化标志
_initialized = False

def _format_extra(record):
    """格式化extra字段"""
    extra = record.get("extra", {})
    if not extra:
        return ""
    
    # 将extra字典转换为可读格式
    extra_str = " ".join([f"{k}={v}" for k, v in extra.items()])
    return f"[{extra_str}]" if extra_str else ""

def _init_logger():
    """初始化logger配置"""
    global _initialized
    if _initialized:
        return
    
    # 移除默认handler
    logger.remove()
    
    # 获取配置
    try:
        # 设置环境变量
        import os
        env = os.environ.get('DJANGO_ENV', 'dev')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'Rookie.settings.{env}')
        
        from django.conf import settings
        config = getattr(settings, 'LOGURU_CONFIG', {})
    except:
        # 如果Django未初始化，使用默认配置
        BASE_DIR = Path(__file__).resolve().parent.parent
        config = {
            'console': {'enabled': True, 'level': 'INFO'},
            'file': {'enabled': True, 'level': 'DEBUG', 'path': BASE_DIR / 'logs' / 'app.log'},
            'error_file': {'enabled': True, 'level': 'ERROR', 'path': BASE_DIR / 'logs' / 'error.log'}
        }
    
    # 配置控制台输出
    console_config = config.get('console', {})
    if console_config.get('enabled', True):
        # 检查是否有自定义格式
        if 'format' in console_config:
            logger.add(
                sys.stdout,
                format=console_config['format'],
                level=console_config.get('level', 'INFO')
            )
        else:
            # 使用默认格式化函数
            def console_format(record):
                extra_str = _format_extra(record)
                return f"<green>{record['time']:YYYY-MM-DD HH:mm:ss}</green> | <level>{record['level']: <8}</level> | <cyan>{record['name']}</cyan>:<cyan>{record['function']}</cyan>:<cyan>{record['line']}</cyan> {extra_str} - <level>{record['message']}</level>\n"
            
            logger.add(
                sys.stdout,
                format=console_format,
                level=console_config.get('level', 'INFO')
            )
    
    # 配置文件输出
    file_config = config.get('file', {})
    if file_config.get('enabled', True):
        file_path = file_config.get('path')
        if file_path:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 检查是否有自定义格式
            if 'format' in file_config:
                logger.add(
                    file_path,
                    format=file_config['format'],
                    level=file_config.get('level', 'DEBUG'),
                    rotation=file_config.get('rotation', '10 MB'),
                    retention=file_config.get('retention', '30 days'),
                    compression=file_config.get('compression', 'zip')
                )
            else:
                # 使用默认格式化函数
                def file_format(record):
                    extra_str = _format_extra(record)
                    return f"{record['time']:YYYY-MM-DD HH:mm:ss} | {record['level']: <8} | {record['name']}:{record['function']}:{record['line']} {extra_str} - {record['message']}\n"
                
                logger.add(
                    file_path,
                    format=file_format,
                    level=file_config.get('level', 'DEBUG'),
                    rotation=file_config.get('rotation', '10 MB'),
                    retention=file_config.get('retention', '30 days'),
                    compression=file_config.get('compression', 'zip')
                )
    
    # 配置错误文件输出
    error_config = config.get('error_file', {})
    if error_config.get('enabled', True):
        error_path = error_config.get('path')
        if error_path:
            Path(error_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 检查是否有自定义格式
            if 'format' in error_config:
                logger.add(
                    error_path,
                    format=error_config['format'],
                    level=error_config.get('level', 'ERROR'),
                    rotation=error_config.get('rotation', '10 MB'),
                    retention=error_config.get('retention', '30 days'),
                    compression=error_config.get('compression', 'zip')
                )
            else:
                # 使用默认格式化函数
                def error_format(record):
                    extra_str = _format_extra(record)
                    return f"{record['time']:YYYY-MM-DD HH:mm:ss} | {record['level']: <8} | {record['name']}:{record['function']}:{record['line']} {extra_str} - {record['message']}\n"
                
                logger.add(
                    error_path,
                    format=error_format,
                    level=error_config.get('level', 'ERROR'),
                    rotation=error_config.get('rotation', '10 MB'),
                    retention=error_config.get('retention', '30 days'),
                    compression=error_config.get('compression', 'zip')
                )
    
    _initialized = True

def reset_logger():
    """重置 logger 配置（用于动态更改配置）"""
    global _initialized
    _initialized = False
    logger.remove()
    _init_logger()

def get_logger():
    """
    获取配置好的loguru logger实例
    
    Returns:
        loguru.Logger: 配置好的logger实例
    """
    _init_logger()
    return logger