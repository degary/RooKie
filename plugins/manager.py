"""
插件管理器
"""
from typing import Dict, List, Optional, Type
from .base import BaseAuthPlugin
from .dingtalk import DingTalkAuthPlugin
from .wechat_work import WeChatWorkAuthPlugin
from utils.logger import get_logger

logger = get_logger()


class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self._plugins: Dict[str, Type[BaseAuthPlugin]] = {}
        self._instances: Dict[str, BaseAuthPlugin] = {}
        self._initialized = False
    
    def _ensure_initialized(self):
        """确保插件已初始化"""
        if not self._initialized:
            self._register_builtin_plugins()
            self._initialized = True
    
    def _register_builtin_plugins(self):
        """注册内置插件"""
        self.register_plugin(DingTalkAuthPlugin)
        self.register_plugin(WeChatWorkAuthPlugin)
    
    def register_plugin(self, plugin_class: Type[BaseAuthPlugin]):
        """注册插件"""
        plugin_name = plugin_class.__name__.lower().replace('authplugin', '')
        self._plugins[plugin_name] = plugin_class
        logger.info(f"注册插件: {plugin_name}")
    
    def get_plugin(self, name: str, config: Dict) -> Optional[BaseAuthPlugin]:
        """获取插件实例"""
        self._ensure_initialized()
        
        if name in self._instances:
            return self._instances[name]
        
        if name not in self._plugins:
            logger.error(f"插件不存在: {name}")
            return None
        
        try:
            plugin_class = self._plugins[name]
            instance = plugin_class(config)
            
            if not instance.validate_config():
                logger.error(f"插件配置无效: {name}")
                return None
            
            self._instances[name] = instance
            return instance
        except Exception as e:
            logger.error(f"创建插件实例失败: {name}", error=str(e))
            return None
    
    def get_available_plugins(self) -> List[str]:
        """获取可用插件列表"""
        self._ensure_initialized()
        return list(self._plugins.keys())
    
    def get_enabled_plugins(self, config: Dict) -> List[BaseAuthPlugin]:
        """获取已启用的插件实例"""
        self._ensure_initialized()
        enabled_plugins = []
        
        for plugin_name, plugin_config in config.items():
            if plugin_config.get('enabled', False):
                plugin = self.get_plugin(plugin_name, plugin_config)
                if plugin:
                    enabled_plugins.append(plugin)
        
        return enabled_plugins


# 全局插件管理器实例
plugin_manager = PluginManager()