# 系统架构

## 📋 概述

Rookie 项目采用经典的 Django MVC 架构模式，结合 DRF 提供 RESTful API 服务，支持多种认证方式和精细化权限控制。

## 🏗️ 整体架构

### 架构图
```
┌─────────────────────────────────────────────────────────────┐
│                        客户端层                              │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Web浏览器     │    移动应用     │      第三方系统         │
│  (Session认证)  │  (Token认证)    │    (API Key认证)        │
└─────────────────┴─────────────────┴─────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                      网关/负载均衡                           │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                      Django应用层                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web视图   │  │  API视图    │  │    管理后台         │  │
│  │ (Templates) │  │   (DRF)     │  │   (SimpleUI)        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  认证中间件 │  │  权限中间件 │  │   响应中间件        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  业务逻辑层 │  │   服务层    │  │     工具层          │  │
│  │  (Models)   │  │ (Services)  │  │    (Utils)          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                       数据层                                │
├─────────────────┬─────────────────┬─────────────────────────┤
│    关系数据库   │      缓存       │        文件存储         │
│ (PostgreSQL/    │     (Redis)     │      (本地/云存储)      │
│   SQLite)       │                 │                         │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### 技术栈
- **Web框架**: Django 4.2+
- **API框架**: Django REST Framework 3.14+
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **缓存**: Redis (可选)
- **认证**: Token + Session + 第三方OAuth
- **权限**: Django原生权限系统 + 自定义模块权限
- **日志**: Loguru
- **管理界面**: SimpleUI (基于Ant Design)

## 📦 模块架构

### 核心模块

#### 1. 用户模块 (users/)
```python
users/
├── models.py              # 用户模型定义
│   ├── User               # 自定义用户模型
│   ├── UserProfile        # 用户资料扩展
│   ├── SystemModule       # 系统模块定义
│   ├── ModulePermission   # 模块权限关联
│   └── ThirdPartyAuthConfig # 第三方登录配置
├── views.py               # API视图
│   └── UserViewSet        # 用户管理ViewSet
├── serializers.py         # 数据序列化器
├── admin.py               # Admin后台配置
├── permissions.py         # 权限检查器
└── urls.py                # 路由配置
```

**核心功能**:
- 用户注册、登录、登出
- 用户信息管理
- 权限模块管理
- 第三方登录集成

#### 2. 工具模块 (utils/)
```python
utils/
├── response/              # 响应包装器
│   ├── wrapper.py         # ApiResponse核心类
│   ├── exceptions.py      # 自定义异常
│   ├── decorators.py      # 响应装饰器
│   └── middleware.py      # 响应中间件
├── auth/                  # 认证权限工具
│   └── permissions.py     # 权限检查工具
└── logger.py              # 日志配置
```

**核心功能**:
- 统一API响应格式
- 权限检查和装饰器
- 日志记录和管理
- 异常处理

#### 3. 插件模块 (plugins/)
```python
plugins/
├── base.py                # 插件基类
├── manager.py             # 插件管理器
├── dingtalk.py            # 钉钉登录插件
├── wechat_work.py         # 企业微信插件
└── feishu.py              # 飞书插件
```

**核心功能**:
- 第三方登录插件架构
- 统一的OAuth处理流程
- 用户信息同步

## 🔄 数据流架构

### 请求处理流程
```
1. 客户端请求
   ↓
2. Django中间件处理
   ├── SecurityMiddleware (安全)
   ├── SessionMiddleware (会话)
   ├── AuthenticationMiddleware (认证)
   └── ResponseMiddleware (响应格式化)
   ↓
3. URL路由匹配
   ↓
4. 视图权限检查
   ├── 认证检查 (Token/Session)
   ├── 权限检查 (模块权限)
   └── 业务权限检查
   ↓
5. 业务逻辑处理
   ├── 数据验证 (Serializers)
   ├── 业务处理 (Models/Services)
   └── 数据库操作 (ORM)
   ↓
6. 响应数据封装
   ├── 数据序列化
   ├── 响应格式统一
   └── 错误处理
   ↓
7. 返回客户端
```

### 认证流程
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   客户端请求    │───▶│   认证中间件    │───▶│   权限检查      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Token/Session   │    │   用户验证      │    │   模块权限      │
│     验证        │    │                 │    │     检查        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   认证成功      │    │   用户激活      │    │   权限通过      │
│                 │    │     检查        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🗄️ 数据库设计

### 核心表结构

#### 用户相关表
```sql
-- 用户表 (继承Django AbstractUser)
users_user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    username VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    avatar VARCHAR(200),
    department VARCHAR(100),
    job_title VARCHAR(100),
    employee_id VARCHAR(50),
    auth_source VARCHAR(20) DEFAULT 'local',
    external_id VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP,
    last_login TIMESTAMP
);

-- 用户资料扩展表
users_userprofile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users_user(id),
    bio TEXT,
    preferences JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 系统模块表
users_systemmodule (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    url_pattern VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP
);

-- 第三方认证配置表
users_thirdpartyauthconfig (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    config JSONB NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### 权限相关表 (Django内置)
```sql
-- 权限表
auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER,
    codename VARCHAR(100) NOT NULL
);

-- 用户组表
auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL
);

-- 用户组权限关联表
auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES auth_group(id),
    permission_id INTEGER REFERENCES auth_permission(id)
);

-- 用户权限关联表
users_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users_user(id),
    permission_id INTEGER REFERENCES auth_permission(id)
);
```

### 数据关系图
```
users_user ──┬── users_userprofile (1:1)
             ├── auth_user_groups (M:N)
             ├── auth_user_user_permissions (M:N)
             └── authtoken_token (1:1)

auth_group ──── auth_group_permissions ──── auth_permission

users_systemmodule ──── auth_permission (通过content_type关联)

users_thirdpartyauthconfig (独立表)
```

## 🔌 插件架构

### 插件系统设计
```python
# 插件基类
class BaseAuthPlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """显示名称"""
        pass
    
    @abstractmethod
    def get_auth_url(self) -> str:
        """获取授权URL"""
        pass
    
    @abstractmethod
    def get_user_info(self, code: str) -> Dict[str, Any]:
        """获取用户信息"""
        pass
    
    def sync_users(self) -> int:
        """同步用户（可选实现）"""
        return 0
```

### 插件管理器
```python
class PluginManager:
    def __init__(self):
        self._plugins = {}
        self._load_plugins()
    
    def register_plugin(self, plugin_class):
        """注册插件"""
        plugin = plugin_class()
        self._plugins[plugin.name] = plugin
    
    def get_plugin(self, name: str, config: Dict) -> BaseAuthPlugin:
        """获取插件实例"""
        if name in self._plugins:
            plugin = self._plugins[name]
            plugin.config = config
            return plugin
        return None
```

## 🔒 安全架构

### 认证安全
- **Token认证**: 40位随机字符串，服务器端存储
- **Session认证**: Django内置Session机制
- **第三方OAuth**: 标准OAuth 2.0流程

### 权限安全
- **模块级权限**: 基于Django权限系统的扩展
- **用户组权限**: 支持用户组和直接用户权限
- **权限继承**: 用户组权限 + 用户直接权限

### 数据安全
- **密码加密**: Django内置PBKDF2算法
- **SQL注入防护**: Django ORM自动防护
- **XSS防护**: 模板自动转义
- **CSRF防护**: Django内置CSRF中间件

## 📈 性能架构

### 数据库优化
- **查询优化**: 使用select_related和prefetch_related
- **索引优化**: 关键字段添加数据库索引
- **连接池**: 生产环境使用数据库连接池

### 缓存策略
- **查询缓存**: 频繁查询的数据缓存
- **权限缓存**: 用户权限信息缓存
- **Session缓存**: Session数据缓存

### 代码优化
- **懒加载**: 按需加载数据
- **批量操作**: 减少数据库查询次数
- **异步处理**: 耗时操作异步执行

## 🔧 扩展架构

### 水平扩展
- **负载均衡**: 多实例部署
- **数据库分离**: 读写分离
- **静态文件分离**: CDN加速

### 功能扩展
- **插件系统**: 第三方登录插件
- **中间件扩展**: 自定义中间件
- **API扩展**: 新增业务模块

### 集成扩展
- **消息队列**: Celery + Redis
- **搜索引擎**: Elasticsearch
- **监控系统**: Prometheus + Grafana

## 🔗 相关文档

- [模块设计](modules.md) - 各模块详细设计
- [编码规范](coding-standards.md) - 代码规范和最佳实践
- [部署指南](deployment.md) - 部署架构和配置