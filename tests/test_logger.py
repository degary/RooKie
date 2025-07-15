#!/usr/bin/env python
"""
测试日志格式输出
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rookie.settings.dev')
django.setup()

from utils.logger import get_logger

def test_logger_formats():
    """测试各种日志格式"""
    logger = get_logger()
    
    print("=== 测试日志格式输出 ===\n")
    
    # 1. 简单消息
    logger.info("简单日志消息")
    
    # 2. 带简单extra参数
    logger.info("带参数的日志", userId="123", email="test@example.com")
    
    # 3. 带复杂字典的extra
    complex_dict = {
        'errcode': 0,
        'errmsg': 'ok',
        'user_info': {
            'nick': '邓辉',
            'unionid': 'HniiFmxDLzu3UPMLadA3TagiEiE',
            'mobile': '16601135746'
        }
    }
    logger.info("复杂字典日志", result=complex_dict)
    
    # 4. 带列表的extra
    list_data = ['item1', 'item2', {'nested': 'value'}]
    logger.info("列表数据日志", items=list_data)
    
    # 5. 带特殊字符的数据
    special_data = {
        'message': "包含'单引号'和\"双引号\"的数据",
        'symbols': '{brackets}',
        'unicode': '中文测试🚀'
    }
    logger.info("特殊字符日志", data=special_data)
    
    # 5.1. 带中括号的数据
    bracket_data = {
        'array': '[item1, item2, item3]',
        'nested': '[[nested], [array]]',
        'mixed': '{key: [value1, value2]}'
    }
    logger.info("中括号测试日志", brackets=bracket_data)
    
    # 5.2. 纯中括号字符串测试
    logger.info("纯中括号测试", data="[test]", array=[1, 2, 3])
    
    # 5.1. 带中括号的数据
    bracket_data = {
        'array': '[item1, item2, item3]',
        'nested': '[[nested], [array]]',
        'mixed': '{key: [value1, value2]}'
    }
    logger.info("中括号测试日志", brackets=bracket_data)
    
    # 6. 纯中括号字符串测试
    logger.info("纯中括号测试", data="[test]", array=[1, 2, 3])
    
    # 7. 超长数据
    long_data = {'key' + str(i): f'value_{i}' * 10 for i in range(20)}
    logger.info("超长数据日志", long_data=long_data)
    
    # 7. 不可序列化的对象
    class CustomObject:
        def __init__(self):
            self.name = "test"
    
    logger.info("不可序列化对象", obj=CustomObject())
    
    # 8. 不同日志级别
    logger.debug("调试信息", level="debug")
    logger.warning("警告信息", level="warning") 
    logger.error("错误信息", level="error")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_logger_formats()