# Utils 工具模块

## 📁 目录结构

```
utils/
├── __init__.py           # 模块入口
├── logger.py             # 日志工具
├── README.md             # 本文档
├── auth/                 # 认证和权限
│   ├── __init__.py
│   └── permissions.py    # 权限检查工具
├── response/             # 响应包装器
│   ├── __init__.py
│   ├── wrapper.py        # 响应包装器核心
│   ├── exceptions.py     # 自定义异常
│   ├── decorators.py     # 装饰器
│   ├── middleware.py     # 中间件
│   └── README.md         # 详细使用文档
├── validation/           # 数据验证（待扩展）
├── cache/                # 缓存工具（待扩展）
└── email/                # 邮件工具（待扩展）
```

## 🚀 快速导入

```python
# 从根模块导入常用工具
from utils import (
    get_logger,           # 日志工具
    ApiResponse,          # 响应包装器
    permission_checker,   # 权限检查器
    require_module_permission,  # 权限装饰器
    ModulePermissionMixin      # 权限混入类
)

# 从子模块导入
from utils.response import ApiResponse, ApiException
from utils.auth import permission_checker
```

## 📚 模块说明

### 1. 日志工具 (logger.py)
```python
from utils import get_logger

logger = get_logger()
logger.info("操作成功", user_id=123)
```

### 2. 响应包装器 (response/)
统一API响应格式，支持成功/错误响应包装。
详见：[response/README.md](response/README.md)

```python
from utils import ApiResponse

# API视图
return ApiResponse.success(data=user_data).to_response()

# 普通函数
return ApiResponse.success(data=result)
```

### 3. 权限工具 (auth/)
模块级权限检查和装饰器。

```python
from utils import permission_checker, require_module_permission

# 检查权限
if permission_checker.has_module_permission(user, 'user_management', 'view'):
    # 有权限的操作

# 装饰器
@require_module_permission('user_management', 'view')
def user_list(request):
    pass
```

## 🔧 扩展指南

### 添加新工具模块

1. **创建目录**
```bash
mkdir utils/new_module
touch utils/new_module/__init__.py
```

2. **实现功能**
```python
# utils/new_module/core.py
class NewTool:
    def do_something(self):
        pass
```

3. **导出接口**
```python
# utils/new_module/__init__.py
from .core import NewTool

__all__ = ['NewTool']
```

4. **更新主模块**
```python
# utils/__init__.py
from .new_module import NewTool

__all__ = [
    # ... 其他导出
    'NewTool'
]
```

### 命名规范

- **文件名**: 小写字母+下划线 (`user_service.py`)
- **类名**: 大驼峰 (`UserService`)
- **函数名**: 小写字母+下划线 (`get_user_info`)
- **常量**: 大写字母+下划线 (`MAX_RETRY_COUNT`)

### 文档规范

每个工具模块都应包含：
- 功能说明
- 使用示例
- API参考
- 注意事项

## 🎯 最佳实践

1. **单一职责**: 每个工具模块专注一个功能领域
2. **向后兼容**: 新版本保持API兼容性
3. **异常处理**: 提供清晰的错误信息
4. **性能考虑**: 避免不必要的计算和内存占用
5. **测试覆盖**: 为工具函数编写单元测试

## 📝 待扩展功能

- [ ] **validation/**: 数据验证工具
- [ ] **cache/**: 缓存管理工具
- [ ] **email/**: 邮件发送工具
- [ ] **file/**: 文件处理工具
- [ ] **crypto/**: 加密解密工具
- [ ] **http/**: HTTP客户端工具