"""
钉钉插件包
"""
from .auth import DingtalkAuthPlugin

# 保持向后兼容
DingTalkAuthPlugin = DingtalkAuthPlugin

__all__ = ['DingtalkAuthPlugin', 'DingTalkAuthPlugin']