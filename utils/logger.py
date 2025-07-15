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
    
    # 将extra字典转换为可读格式，处理复杂数据结构
    def safe_str(value):
        try:
            if isinstance(value, (dict, list)):
                import json
                # 转义花括号避免与Loguru格式化冲突
                json_str = json.dumps(value, ensure_ascii=False, default=str)
                return json_str.replace('{', '{{').replace('}', '}}')
            return str(value)
        except:
            return "<unprintable>"
    
    extra_str = " ".join([f"{k}={safe_str(v)}" for k, v in extra.items()])
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
        def console_formatter(record):
            extra = record.get('extra', {})
            extra_str = ''
            if extra:
                extra_parts = []
                for k, v in extra.items():
                    if k not in ['name', 'function', 'line', 'level', 'time', 'message']:
                        try:
                            # 安全地转换复杂数据类型
                            if isinstance(v, (dict, list)):
                                import json
                                v_str = json.dumps(v, ensure_ascii=False, separators=(',', ':'))[:100]
                                if len(str(v)) > 100:
                                    v_str += '...'
                                # 转义特殊字符避免Loguru格式化错误
                                v_str = v_str.replace('{', '{{').replace('}', '}}').replace('<', '&lt;').replace('>', '&gt;')
                            else:
                                v_str = str(v).replace('{', '{{').replace('}', '}}').replace('<', '&lt;').replace('>', '&gt;')
                            extra_parts.append(f"{k}={v_str}")
                        except Exception:
                            extra_parts.append(f"{k}=&lt;unprintable&gt;")
                if extra_parts:
                    extra_str = f" [{' '.join(extra_parts)}]"
            
            try:
                from colorama import Fore, Style
                time_str = f"{Fore.GREEN}{record['time'].strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}"
                level_color = {'DEBUG': Fore.BLUE, 'INFO': Fore.CYAN, 'WARNING': Fore.YELLOW, 'ERROR': Fore.RED, 'CRITICAL': Fore.MAGENTA}.get(record['level'].name, '')
                level_str = f"{level_color}{record['level']: <8}{Style.RESET_ALL}"
                location_str = f"{Fore.CYAN}{record['name']}:{record['function']}:{record['line']}{Style.RESET_ALL}"
                message_str = f"{level_color}{record['message']}{Style.RESET_ALL}"
            except ImportError:
                time_str = record['time'].strftime('%Y-%m-%d %H:%M:%S')
                level_str = f"{record['level']: <8}"
                location_str = f"{record['name']}:{record['function']}:{record['line']}"
                message_str = record['message']
            
            return f"{time_str} | {level_str} | {location_str}{extra_str} - {message_str}\n"
        
        logger.add(
            sys.stdout,
            format=console_formatter,
            level=console_config.get('level', 'INFO')
        )

    
    # 配置文件输出
    file_config = config.get('file', {})
    if file_config.get('enabled', True):
        file_path = file_config.get('path')
        if file_path:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            logger.add(
                file_path,
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
            logger.add(
                error_path,
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