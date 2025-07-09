# 模块设计详解

## 📋 概述

本文档详细介绍 Rookie 项目各个模块的设计思路、实现方法和使用指南，帮助开发者深入理解和扩展项目功能。

## 👥 用户模块 (users/)

### 模块结构
```
users/
├── models.py              # 数据模型
├── views.py               # API视图
├── serializers.py         # 序列化器
├── admin.py               # 管理后台
├── urls.py                # 路由配置
├── permissions.py         # 权限检查
├── forms.py               # 表单定义
├── login_views.py         # 登录页面视图
├── migrations/            # 数据库迁移
└── tests.py               # 测试用例
```

### 核心模型设计

#### User模型
```python
class User(AbstractUser):
    """自定义用户模型"""
    
    # 基础字段
    email = models.EmailField(unique=True, verbose_name="邮箱")
    username = models.CharField(max_length=150, verbose_name="用户名")
    phone = models.CharField(max_length=20, blank=True, verbose_name="手机号")
    
    # 扩展字段
    avatar = models.URLField(blank=True, verbose_name="头像")
    department = models.CharField(max_length=100, blank=True, verbose_name="部门")
    job_title = models.CharField(max_length=100, blank=True, verbose_name="职位")
    employee_id = models.CharField(max_length=50, blank=True, verbose_name="员工编号")
    
    # 第三方登录字段
    auth_source = models.CharField(max_length=20, default='local', verbose_name="认证来源")
    external_id = models.CharField(max_length=100, blank=True, verbose_name="外部ID")
    
    # 状态字段
    is_verified = models.BooleanField(default=False, verbose_name="邮箱已验证")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        db_table = 'users_user'
```

**设计要点**:
- 使用邮箱作为登录标识
- 支持第三方登录信息存储
- 扩展企业级用户信息字段
- 保持与Django权限系统兼容

#### UserProfile模型
```python
class UserProfile(models.Model):
    """用户资料扩展"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    bio = models.TextField(blank=True, verbose_name="个人简介")
    preferences = models.JSONField(default=dict, verbose_name="个人偏好")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"
```

**设计要点**:
- 一对一关联用户模型
- 使用JSONField存储灵活配置
- 分离核心用户信息和扩展信息

#### SystemModule模型
```python
class SystemModule(models.Model):
    """系统模块定义"""
    
    name = models.CharField(max_length=50, unique=True, verbose_name="模块名称")
    display_name = models.CharField(max_length=100, verbose_name="显示名称")
    description = models.TextField(blank=True, verbose_name="模块描述")
    icon = models.CharField(max_length=50, blank=True, verbose_name="图标")
    url_pattern = models.CharField(max_length=200, blank=True, verbose_name="URL模式")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "系统模块"
        verbose_name_plural = "系统模块"
        permissions = [
            ('view_systemmodule', '可以查看系统模块'),
            ('add_systemmodule', '可以添加系统模块'),
            ('change_systemmodule', '可以修改系统模块'),
            ('delete_systemmodule', '可以删除系统模块'),
        ]
```

**设计要点**:
- 定义系统功能模块
- 与Django权限系统集成
- 支持图标和URL配置

### API视图设计

#### UserViewSet
```python
class UserViewSet(viewsets.ModelViewSet):
    """用户管理ViewSet"""
    
    queryset = User.objects.active_users()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """动态权限配置"""
        if self.action in ['register', 'login', 'third_party_auth', 'third_party_callback']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册"""
        # 实现用户注册逻辑
        pass
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        # 实现用户登录逻辑，返回Token
        pass
    
    @action(detail=False, methods=['get'])
    def my_modules(self, request):
        """获取用户权限模块"""
        # 返回用户可访问的模块和权限
        pass
```

**设计要点**:
- 使用ViewSet提供完整的CRUD操作
- 动态权限配置支持公开和私有接口
- 自定义action扩展业务功能
- 统一使用ApiResponse格式

### 权限系统设计

#### 权限检查器
```python
class PermissionChecker:
    """权限检查器"""
    
    def has_module_permission(self, user, module_name: str, permission_type: str) -> bool:
        """检查用户是否有模块权限"""
        if user.is_superuser:
            return True
        
        # 检查用户直接权限
        codename = f"{permission_type}_systemmodule"
        if user.has_perm(f"users.{codename}"):
            return True
        
        # 检查用户组权限
        return user.groups.filter(
            permissions__codename=codename,
            permissions__content_type__app_label='users'
        ).exists()
    
    def get_user_modules(self, user):
        """获取用户可访问的模块"""
        if user.is_superuser:
            return SystemModule.objects.filter(is_active=True)
        
        # 获取用户有权限的模块
        user_permissions = self.get_user_permissions(user)
        if 'view_systemmodule' in user_permissions:
            return SystemModule.objects.filter(is_active=True)
        
        return SystemModule.objects.none()
```

#### 权限装饰器
```python
def require_module_permission(module_name: str, permission_type: str):
    """模块权限装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if not permission_checker.has_module_permission(
                request.user, module_name, permission_type
            ):
                return ApiResponse.forbidden(
                    f'需要{module_name}模块的{permission_type}权限'
                ).to_response()
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
```

**设计要点**:
- 基于Django原生权限系统扩展
- 支持模块级权限控制
- 提供装饰器和混入类两种使用方式
- 权限检查逻辑可复用

## 🛠️ 工具模块 (utils/)

### 响应包装器 (response/)

#### 核心设计
```python
class ApiResponse:
    """API响应包装器"""
    
    def __init__(self, success: bool, code: int, message: str, data=None, request_id: str = None):
        self.success = success
        self.code = code
        self.message = message
        self.data = data
        self.timestamp = timezone.now().isoformat()
        self.request_id = request_id or str(uuid.uuid4())[:8]
    
    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            'success': self.success,
            'code': self.code,
            'message': self.message,
            'timestamp': self.timestamp,
            'request_id': self.request_id
        }
        if self.data is not None:
            result['data'] = self.data
        return result
    
    def to_response(self) -> Response:
        """转换为DRF Response对象"""
        return Response(
            data=self.to_dict(),
            status=self.code if self.code < 600 else 200
        )
    
    @classmethod
    def success(cls, data=None, message: str = "操作成功", code: int = 200):
        """成功响应"""
        return cls(success=True, code=code, message=message, data=data)
    
    @classmethod
    def error(cls, message: str = "操作失败", code: int = 400, data=None):
        """错误响应"""
        return cls(success=False, code=code, message=message, data=data)
```

**设计要点**:
- 统一所有API响应格式
- 支持链式调用和类方法
- 自动生成时间戳和请求ID
- 兼容DRF Response对象

#### 异常处理
```python
def custom_exception_handler(exc, context):
    """自定义异常处理器"""
    
    # 处理自定义异常
    if isinstance(exc, ApiException):
        response = ApiResponse.error(
            message=exc.message,
            code=exc.code,
            data=exc.data
        )
        return response.to_response()
    
    # 处理DRF默认异常
    response = exception_handler(exc, context)
    
    if response is not None:
        # 包装DRF异常响应
        if response.status_code == 400:
            api_response = ApiResponse.bad_request(
                message="请求参数错误",
                data=response.data
            )
        elif response.status_code == 401:
            api_response = ApiResponse.unauthorized()
        # ... 其他状态码处理
        
        return Response(
            data=api_response.to_dict(),
            status=response.status_code
        )
    
    return response
```

### 日志模块 (logger.py)

#### 日志配置
```python
def setup_logger():
    """配置Loguru日志"""
    
    # 移除默认处理器
    logger.remove()
    
    # 根据环境配置不同的日志处理器
    env = os.getenv('DJANGO_ENV', 'dev')
    
    if env == 'dev':
        # 开发环境：控制台 + 文件
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG",
            colorize=True
        )
        logger.add(
            "logs/dev.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="INFO",
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )
    elif env == 'prod':
        # 生产环境：仅文件
        logger.add(
            "/var/log/rookie/app.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="INFO",
            rotation="50 MB",
            retention="30 days",
            compression="zip"
        )
    
    return logger

def get_logger(name: str = None):
    """获取日志器实例"""
    if name:
        return logger.bind(name=name)
    return logger
```

**设计要点**:
- 基于Loguru的高性能日志系统
- 支持多环境配置
- 自动日志轮转和压缩
- 结构化日志支持

## 🔌 插件模块 (plugins/)

### 插件架构设计

#### 基础插件类
```python
class BaseAuthPlugin(ABC):
    """第三方认证插件基类"""
    
    def __init__(self):
        self.config = {}
    
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
        """根据授权码获取用户信息"""
        pass
    
    def get_qr_code_url(self) -> str:
        """获取二维码URL（可选实现）"""
        return self.get_auth_url()
    
    def sync_users(self) -> int:
        """同步用户（可选实现）"""
        return 0
    
    def validate_config(self, config: Dict) -> bool:
        """验证配置（可选实现）"""
        return True
```

#### 钉钉插件实现
```python
class DingTalkAuthPlugin(BaseAuthPlugin):
    """钉钉登录插件"""
    
    @property
    def name(self) -> str:
        return 'dingtalk'
    
    @property
    def display_name(self) -> str:
        return '钉钉登录'
    
    def get_auth_url(self) -> str:
        """生成钉钉授权URL"""
        app_id = self.config.get('app_id')
        redirect_uri = self.config.get('redirect_uri')
        
        params = {
            'appid': app_id,
            'response_type': 'code',
            'scope': 'snsapi_login',
            'state': 'dingtalk_login',
            'redirect_uri': redirect_uri
        }
        
        return f"https://oapi.dingtalk.com/connect/oauth2/sns_authorize?{urlencode(params)}"
    
    def get_user_info(self, code: str) -> Dict[str, Any]:
        """获取钉钉用户信息"""
        # 1. 获取access_token
        token_data = self._get_access_token(code)
        access_token = token_data.get('access_token')
        
        # 2. 获取用户信息
        user_info = self._get_user_profile(access_token)
        
        # 3. 标准化用户信息
        return {
            'source': 'dingtalk',
            'external_id': user_info.get('openid'),
            'username': user_info.get('nick'),
            'email': user_info.get('email'),
            'phone': user_info.get('mobile'),
            'avatar': user_info.get('avatarUrl'),
            'department': user_info.get('dept_name'),
            'job_title': user_info.get('position'),
            'employee_id': user_info.get('job_number')
        }
    
    def _get_access_token(self, code: str) -> Dict:
        """获取访问令牌"""
        # 实现获取access_token的逻辑
        pass
    
    def _get_user_profile(self, access_token: str) -> Dict:
        """获取用户资料"""
        # 实现获取用户信息的逻辑
        pass
```

#### 插件管理器
```python
class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self._plugins = {}
        self._load_plugins()
    
    def _load_plugins(self):
        """加载所有插件"""
        # 自动发现和注册插件
        plugin_classes = [
            DingTalkAuthPlugin,
            WeChatWorkAuthPlugin,
            FeishuAuthPlugin,
        ]
        
        for plugin_class in plugin_classes:
            self.register_plugin(plugin_class)
    
    def register_plugin(self, plugin_class):
        """注册插件"""
        plugin = plugin_class()
        self._plugins[plugin.name] = plugin
        logger.info(f"注册插件: {plugin.display_name}")
    
    def get_plugin(self, name: str, config: Dict) -> BaseAuthPlugin:
        """获取插件实例"""
        if name in self._plugins:
            plugin = self._plugins[name]
            plugin.config = config
            return plugin
        return None
    
    def list_plugins(self) -> List[str]:
        """列出所有插件"""
        return list(self._plugins.keys())

# 全局插件管理器实例
plugin_manager = PluginManager()
```

**设计要点**:
- 基于抽象基类的插件架构
- 统一的用户信息格式
- 自动插件发现和注册
- 配置验证和错误处理

## 📱 模板模块 (templates/)

### 模板结构
```
templates/
├── auth/                  # 认证相关页面
│   └── login.html         # 登录页面
├── admin/                 # 管理后台模板
├── users/                 # 用户相关页面
├── common/                # 通用组件
│   ├── base.html          # 基础模板
│   ├── header.html        # 页头组件
│   └── footer.html        # 页脚组件
└── errors/                # 错误页面
    ├── 404.html           # 404页面
    ├── 500.html           # 500页面
    └── 403.html           # 403页面
```

### 登录页面设计
```html
<!-- templates/auth/login.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rookie 登录</title>
    <!-- Ant Design风格样式 -->
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="logo">R</div>
            <h1 class="login-title">欢迎使用 Rookie</h1>
            <p class="login-subtitle">企业级应用管理平台</p>
        </div>
        
        <div class="login-tabs">
            <button class="tab-btn active" onclick="switchTab('password')">
                账号登录
            </button>
            <button class="tab-btn" onclick="switchTab('qrcode')">
                扫码登录
            </button>
        </div>
        
        <div class="login-content">
            <!-- 账号登录面板 -->
            <div id="password-panel" class="tab-panel active">
                <form id="login-form">
                    <!-- 登录表单 -->
                </form>
            </div>
            
            <!-- 扫码登录面板 -->
            <div id="qrcode-panel" class="tab-panel">
                <div class="qr-container">
                    <!-- 二维码区域 -->
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 登录逻辑JavaScript代码
    </script>
</body>
</html>
```

**设计要点**:
- Ant Design风格的现代化界面
- 支持账号登录和扫码登录切换
- 响应式设计适配移动端
- 集成第三方登录API

## 🔧 配置模块 (settings/)

### 配置结构
```
Rookie/settings/
├── base.py                # 基础配置
├── dev.py                 # 开发环境
├── acc.py                 # 测试环境
├── prod.py                # 生产环境
└── __init__.py            # 环境选择
```

### 基础配置设计
```python
# settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 应用配置
INSTALLED_APPS = [
    'simpleui',                    # 管理界面美化
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',              # API框架
    'rest_framework.authtoken',    # Token认证
    'users',                       # 用户模块
]

# 中间件配置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DRF配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'utils.response.exceptions.custom_exception_handler'
}

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

# 登录设置
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/admin/'

# SimpleUI配置
SIMPLEUI_DEFAULT_THEME = 'ant.design.css'
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_HOME_TITLE = 'Rookie 管理后台'
```

### 环境配置设计
```python
# settings/dev.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# 开发数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 开发日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'dev.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'users': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

**设计要点**:
- 分环境配置管理
- 基础配置和环境配置分离
- 支持环境变量覆盖
- 详细的日志配置

## 🔗 模块间交互

### 依赖关系图
```
users (核心模块)
├── 依赖 utils (工具模块)
├── 依赖 plugins (插件模块)
└── 被依赖 templates (模板模块)

utils (工具模块)
├── response (响应包装)
├── auth (权限工具)
└── logger (日志工具)

plugins (插件模块)
├── 依赖 users.models
└── 提供第三方登录服务

templates (模板模块)
├── 依赖 users.views
└── 提供前端界面
```

### 接口设计原则
1. **单一职责**: 每个模块专注特定功能
2. **松耦合**: 模块间通过接口交互
3. **高内聚**: 相关功能集中在同一模块
4. **可扩展**: 支持插件和中间件扩展

## 🔗 相关文档

- [系统架构](architecture.md) - 整体架构设计
- [编码规范](coding-standards.md) - 代码规范和最佳实践
- [测试指南](testing.md) - 测试方法和覆盖率要求