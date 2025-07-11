# 权限系统使用指南

## 📋 概述

Rookie项目采用基于Django原生权限系统的模块级权限控制，支持精细化的权限管理。

## 🏗️ 权限架构

### 权限模型
```
系统模块 (SystemModule)
├── 👥 用户管理 (user_management)
├── ⚙️ 系统配置 (system_config)
├── 📊 数据分析 (data_analysis)
├── 📁 文件管理 (file_management)
└── 🔔 消息通知 (notification)

权限类型：
• view    - 可查看
• add     - 可新增  
• change  - 可修改
• delete  - 可删除
```

### 权限分配方式
- **用户组权限**: 为用户组分配权限，用户继承组权限
- **用户直接权限**: 为特定用户单独分配权限（优先级更高）

## 🚀 快速开始

### 1. 初始化权限系统
```bash
# 运行初始化脚本
python examples/setup_permissions.py
```

### 2. 访问Admin后台配置
```bash
# 访问地址
http://127.0.0.1:8000/admin/

# 相关页面
- 用户管理 > 系统模块
- 权限管理 > 用户组  
- 用户管理 > 用户
```

## 🔧 开发使用

### 1. 视图权限控制

#### ViewSet权限配置
```python
from rest_framework import viewsets
from utils.auth.permissions import ModulePermissionMixin

class UserViewSet(ModulePermissionMixin, viewsets.ModelViewSet):
    """用户管理ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # 模块权限配置
    module_name = 'user_management'
    permission_mapping = {
        'list': 'view',
        'retrieve': 'view', 
        'create': 'add',
        'update': 'change',
        'partial_update': 'change',
        'destroy': 'delete'
    }
```

#### 装饰器权限控制
```python
from utils.auth.permissions import require_module_permission

class UserViewSet(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['get'])
    @require_module_permission('user_management', 'view')
    def active_users(self, request):
        """获取活跃用户 - 需要查看权限"""
        users = User.objects.filter(is_active=True)
        return ApiResponse.success(data={'users': UserSerializer(users, many=True).data})
    
    @action(detail=True, methods=['post'])
    @require_module_permission('user_management', 'change')
    def reset_password(self, request, pk=None):
        """重置密码 - 需要修改权限"""
        user = self.get_object()
        # 重置密码逻辑
        return ApiResponse.success(message='密码重置成功')
```

#### 动态权限配置
```python
class UserViewSet(viewsets.ModelViewSet):
    
    def get_permissions(self):
        """根据动作动态设置权限"""
        permission_map = {
            'list': ('user_management', 'view'),
            'create': ('user_management', 'add'),
            'update': ('user_management', 'change'),
            'destroy': ('user_management', 'delete'),
        }
        
        if self.action in permission_map:
            module, perm_type = permission_map[self.action]
            return [IsAuthenticated(), ModulePermission(module, perm_type)]
        
        return [IsAuthenticated()]
```

### 2. 手动权限检查

```python
from utils.auth.permissions import permission_checker

def some_business_logic(user):
    # 检查用户是否有权限
    if permission_checker.has_module_permission(user, 'user_management', 'view'):
        # 有权限的操作
        return get_user_data()
    else:
        # 无权限处理
        raise PermissionDenied('权限不足')

# 获取用户可访问的模块
def get_user_modules(user):
    modules = permission_checker.get_user_modules(user)
    return [module.name for module in modules]
```

### 3. 模板中权限检查

```html
<!-- 检查用户权限 -->
{% if perms.users.view_systemmodule %}
    <a href="/admin/users/">用户管理</a>
{% endif %}

{% if perms.users.add_systemmodule %}
    <button>添加用户</button>
{% endif %}
```

## 📊 权限配置示例

### 1. 创建系统模块

#### 通过Admin后台
1. 访问 `系统模块` 页面
2. 点击 `增加系统模块`
3. 填写模块信息：
   - 名称: `product_management`
   - 显示名称: `产品管理`
   - 描述: `产品信息管理功能`
   - 图标: `fas fa-box`
   - URL模式: `/admin/products/`

#### 通过代码创建
```python
from users.models import SystemModule

module = SystemModule.objects.create(
    name='product_management',
    display_name='产品管理',
    description='产品信息管理功能',
    icon='fas fa-box',
    url_pattern='/admin/products/'
)
```

### 2. 配置用户组权限

#### 通过Admin后台
1. 访问 `用户组` 页面
2. 创建或编辑用户组
3. 在 `权限` 中选择相应的模块权限
4. 保存配置

#### 通过代码配置
```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# 创建用户组
product_managers = Group.objects.create(name='产品经理')

# 获取权限
content_type = ContentType.objects.get_for_model(SystemModule)
permissions = Permission.objects.filter(
    content_type=content_type,
    codename__in=['view_systemmodule', 'add_systemmodule', 'change_systemmodule']
)

# 分配权限
product_managers.permissions.set(permissions)
```

### 3. 分配用户权限

#### 将用户添加到用户组
```python
from users.models import User

user = User.objects.get(email='manager@example.com')
product_managers = Group.objects.get(name='产品经理')
user.groups.add(product_managers)
```

#### 直接为用户分配权限
```python
# 获取特定权限
permission = Permission.objects.get(
    content_type__app_label='users',
    codename='view_systemmodule'
)

# 分配给用户
user.user_permissions.add(permission)
```

## 🔍 权限验证

### 1. API接口测试

```bash
# 获取用户可访问的模块
curl -H "Authorization: Token your_token" \
     http://127.0.0.1:8000/api/users/my_modules/

# 测试需要权限的接口
curl -H "Authorization: Token your_token" \
     http://127.0.0.1:8000/api/users/
```

### 2. Python测试脚本

```python
import requests

def test_permissions():
    # 登录获取Token
    response = requests.post('http://127.0.0.1:8000/api/users/login/', json={
        'email': 'admin@example.com',
        'password': 'password123'
    })
    token = response.json()['data']['token']
    headers = {'Authorization': f'Token {token}'}
    
    # 测试权限接口
    response = requests.get('http://127.0.0.1:8000/api/users/my_modules/', headers=headers)
    modules = response.json()['data']['modules']
    
    print("用户可访问的模块:")
    for module in modules:
        print(f"- {module['display_name']}: {module['permissions']}")
    
    # 测试具体权限
    response = requests.get('http://127.0.0.1:8000/api/users/', headers=headers)
    if response.status_code == 200:
        print("✅ 有用户查看权限")
    else:
        print("❌ 无用户查看权限")

if __name__ == '__main__':
    test_permissions()
```

## 📋 常用权限配置

### 管理员权限
```python
# 所有模块的所有权限
admin_permissions = [
    'user_management.view',
    'user_management.add', 
    'user_management.change',
    'user_management.delete',
    'system_config.view',
    'system_config.change',
    # ... 其他模块权限
]
```

### 部门经理权限
```python
# 部分模块的管理权限
manager_permissions = [
    'user_management.view',
    'user_management.change',
    'data_analysis.view',
    'data_analysis.add',
    'file_management.view',
    'file_management.add',
    'file_management.change',
]
```

### 普通员工权限
```python
# 基础查看权限
employee_permissions = [
    'notification.view',
    'file_management.view',
]
```

## ⚠️ 注意事项

### 1. 权限继承
- 用户直接权限优先于用户组权限
- 超级用户(is_superuser=True)拥有所有权限
- 权限检查会同时考虑用户权限和组权限

### 2. 性能考虑
- 权限检查会查询数据库，在高频接口中注意性能
- 可以考虑缓存用户权限信息
- 避免在循环中进行权限检查

### 3. 安全建议
- 遵循最小权限原则
- 定期审查用户权限
- 重要操作添加额外验证
- 记录权限变更日志

## 🔗 相关文档

- [Django权限系统](https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization)
- [DRF权限控制](https://www.django-rest-framework.org/api-guide/permissions/)
- [项目API文档](../README.md#api-文档)

## 🆘 常见问题

### Q: 如何为新功能添加权限控制？
A: 
1. 创建对应的系统模块
2. 在视图中添加权限检查装饰器
3. 为相关用户组分配权限

### Q: 用户权限不生效怎么办？
A:
1. 检查用户是否在正确的用户组中
2. 确认用户组是否有对应权限
3. 检查权限检查代码是否正确

### Q: 如何批量分配权限？
A: 使用Django管理命令或编写脚本批量处理

### Q: 权限检查影响性能怎么办？
A: 考虑使用缓存或在业务层面优化权限检查逻辑