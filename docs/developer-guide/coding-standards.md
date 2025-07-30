# 编码规范

## 📋 概述

本文档定义了 Rookie 项目的编码规范和最佳实践，确保代码质量和团队协作效率。

## 🐍 Python 代码规范

### 代码风格

我们遵循 [PEP 8](https://pep8.org/) 规范，并使用以下工具：

- **Black**: 自动代码格式化
- **isort**: 导入语句排序
- **flake8**: 代码质量检查
- **mypy**: 类型检查

### 命名约定

```python
# 模块名：小写+下划线
user_management.py

# 类名：大驼峰命名
class UserManager:
    pass

class ThirdPartyAuthConfig:
    pass

# 函数名：小写+下划线
def get_user_profile():
    pass

def authenticate_third_party_user():
    pass

# 变量名：小写+下划线
user_email = "user@example.com"
auth_token = "abc123"

# 常量：大写+下划线
MAX_LOGIN_ATTEMPTS = 5
DEFAULT_PAGE_SIZE = 20

# 私有属性/方法：前缀单下划线
class User:
    def _validate_email(self):
        pass

    def __init__(self):
        self._internal_data = {}

# 特殊方法：双下划线包围
def __str__(self):
    return f"User({self.email})"
```

### 类型注解

```python
from typing import Optional, List, Dict, Any, Union
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def get_permissions(self) -> List[str]:
        """获取用户权限列表"""
        return list(self.user_permissions.values_list('codename', flat=True))

    def has_module_permission(self, module: str, action: str) -> bool:
        """检查模块权限"""
        permission_code = f"{action}_{module}"
        return self.has_perm(permission_code)

def authenticate_user(
    email: str,
    password: str,
    remember_me: bool = False
) -> Optional[User]:
    """
    用户认证

    Args:
        email: 用户邮箱
        password: 密码
        remember_me: 是否记住登录状态

    Returns:
        认证成功返回用户对象，失败返回None
    """
    pass

# API视图类型注解
from rest_framework.request import Request
from rest_framework.response import Response

def login_view(request: Request) -> Response:
    """登录视图"""
    pass
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def sync_third_party_users(
    provider: str,
    department_id: Optional[str] = None,
    force_update: bool = False
) -> Dict[str, Any]:
    """
    同步第三方平台用户信息

    从指定的第三方平台同步用户信息到本地数据库，支持增量同步和全量同步。

    Args:
        provider: 第三方平台名称，如 'dingtalk', 'wechat_work'
        department_id: 部门ID，为空时同步所有部门
        force_update: 是否强制更新已存在的用户信息

    Returns:
        同步结果字典，包含以下字段：
        - success_count: 成功同步的用户数量
        - failed_count: 同步失败的用户数量
        - updated_count: 更新的用户数量
        - created_count: 新创建的用户数量
        - errors: 错误信息列表

    Raises:
        ValueError: 当provider参数无效时
        ConnectionError: 当无法连接第三方平台时
        AuthenticationError: 当第三方平台认证失败时

    Example:
        >>> result = sync_third_party_users('dingtalk', force_update=True)
        >>> print(f"同步成功: {result['success_count']} 个用户")

    Note:
        - 同步过程中会自动处理用户权限分配
        - 建议在低峰期执行大批量同步操作
        - 同步日志会记录到系统日志中
    """
    pass
```

### 异常处理

```python
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from utils.logger import get_logger

logger = get_logger()

def authenticate_third_party_user(code: str, provider: str) -> User:
    """第三方用户认证"""
    try:
        # 获取第三方用户信息
        user_info = get_third_party_user_info(code, provider)

        # 验证用户信息
        if not user_info.get('email'):
            raise ValidationError("第三方平台未返回用户邮箱")

        # 创建或更新用户
        user, created = User.objects.get_or_create(
            email=user_info['email'],
            defaults={
                'username': user_info.get('name', ''),
                'auth_source': provider,
                'external_id': user_info.get('id'),
            }
        )

        logger.info(
            "第三方用户认证成功",
            user_id=user.id,
            provider=provider,
            created=created
        )

        return user

    except ValidationError as e:
        logger.warning("用户信息验证失败", error=str(e), provider=provider)
        raise AuthenticationFailed("用户信息验证失败")

    except ConnectionError as e:
        logger.error("第三方平台连接失败", error=str(e), provider=provider)
        raise AuthenticationFailed("第三方平台连接失败")

    except Exception as e:
        logger.error("第三方认证异常", error=str(e), provider=provider)
        raise AuthenticationFailed("认证服务异常")
```

## 🏗️ Django 最佳实践

### 模型设计

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from utils.models import BaseModel

class User(AbstractUser):
    """自定义用户模型"""

    # 使用邮箱作为登录字段
    email = models.EmailField(
        '邮箱地址',
        unique=True,
        validators=[EmailValidator()]
    )

    # 扩展字段
    phone = models.CharField('手机号', max_length=20, blank=True)
    avatar = models.URLField('头像', blank=True)
    department = models.CharField('部门', max_length=100, blank=True)
    job_title = models.CharField('职位', max_length=100, blank=True)
    employee_id = models.CharField('工号', max_length=50, blank=True)

    # 第三方登录相关
    auth_source = models.CharField(
        '认证来源',
        max_length=20,
        choices=[
            ('local', '本地'),
            ('dingtalk', '钉钉'),
            ('wechat_work', '企业微信'),
            ('feishu', '飞书'),
        ],
        default='local'
    )
    external_id = models.CharField('外部ID', max_length=100, blank=True)

    # 状态字段
    is_verified = models.BooleanField('已验证', default=False)
    last_login_ip = models.GenericIPAddressField('最后登录IP', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['auth_source', 'external_id']),
        ]

    def __str__(self) -> str:
        return f"{self.email} ({self.get_full_name() or self.username})"

    def get_display_name(self) -> str:
        """获取显示名称"""
        return self.get_full_name() or self.username or self.email

    def has_module_permission(self, module: str, action: str) -> bool:
        """检查模块权限"""
        if self.is_superuser:
            return True

        permission_code = f"{action}_{module}"
        return self.has_perm(f"users.{permission_code}")

class SystemModule(BaseModel):
    """系统模块"""

    name = models.CharField('模块名称', max_length=50, unique=True)
    display_name = models.CharField('显示名称', max_length=100)
    description = models.TextField('描述', blank=True)
    icon = models.CharField('图标', max_length=50, blank=True)
    url_pattern = models.CharField('URL模式', max_length=200, blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    sort_order = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'users_system_module'
        verbose_name = '系统模块'
        verbose_name_plural = '系统模块'
        ordering = ['sort_order', 'name']

    def __str__(self) -> str:
        return self.display_name
```

### 视图设计

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from utils.response import ApiResponse
from utils.auth.permissions import ModulePermissionRequired
from .models import User
from .serializers import UserSerializer, LoginSerializer

class UserViewSet(viewsets.ModelViewSet):
    """用户管理ViewSet"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """根据动作设置权限"""
        if self.action == 'login':
            return []  # 登录不需要认证
        elif self.action in ['list', 'retrieve']:
            return [ModulePermissionRequired('user_management', 'view')]
        elif self.action in ['create', 'update', 'partial_update']:
            return [ModulePermissionRequired('user_management', 'edit')]
        elif self.action == 'destroy':
            return [ModulePermissionRequired('user_management', 'delete')]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def login(self, request: Request) -> Response:
        """用户登录"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)
        if not user:
            return ApiResponse.error("登录信息验证失败", code=401)

        if not user.is_active:
            return ApiResponse.error("账户已被禁用", code=403)

        # 记录登录信息
        user.last_login_ip = self.get_client_ip(request)
        user.save(update_fields=['last_login_ip'])

        # 生成Token
        token, created = Token.objects.get_or_create(user=user)

        return ApiResponse.success({
            'token': token.key,
            'user': UserSerializer(user).data
        }, message="登录成功")

    @action(detail=False, methods=['get'])
    def profile(self, request: Request) -> Response:
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=['get'])
    def my_modules(self, request: Request) -> Response:
        """获取当前用户可访问的模块"""
        user = request.user
        modules = []

        for module in SystemModule.objects.filter(is_active=True):
            if user.has_module_permission(module.name, 'view'):
                modules.append({
                    'name': module.name,
                    'display_name': module.display_name,
                    'icon': module.icon,
                    'url_pattern': module.url_pattern,
                })

        return ApiResponse.success(modules)

    def get_client_ip(self, request: Request) -> str:
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
```

### 序列化器设计

```python
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, SystemModule

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    full_name = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'phone', 'avatar', 'department', 'job_title',
            'employee_id', 'auth_source', 'is_active', 'is_verified',
            'date_joined', 'last_login', 'permissions'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'auth_source']

    def get_full_name(self, obj: User) -> str:
        """获取全名"""
        return obj.get_full_name() or obj.username

    def get_permissions(self, obj: User) -> List[str]:
        """获取用户权限"""
        if obj.is_superuser:
            return ['*']  # 超级用户拥有所有权限

        permissions = []
        for module in SystemModule.objects.filter(is_active=True):
            for action in ['view', 'add', 'change', 'delete']:
                if obj.has_module_permission(module.name, action):
                    permissions.append(f"{module.name}.{action}")

        return permissions

class LoginSerializer(serializers.Serializer):
    """登录序列化器"""

    email = serializers.EmailField(label='邮箱')
    password = serializers.CharField(label='密码', write_only=True)
    remember_me = serializers.BooleanField(label='记住我', default=False)

    def validate_email(self, value: str) -> str:
        """验证邮箱"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("用户不存在")
        return value

class PasswordChangeSerializer(serializers.Serializer):
    """修改密码序列化器"""

    old_password = serializers.CharField(label='原密码', write_only=True)
    new_password = serializers.CharField(label='新密码', write_only=True)
    confirm_password = serializers.CharField(label='确认密码', write_only=True)

    def validate_old_password(self, value: str) -> str:
        """验证原密码"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value

    def validate_new_password(self, value: str) -> str:
        """验证新密码"""
        validate_password(value)
        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """验证密码一致性"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return attrs
```

## 🧪 测试规范

### 测试结构

```python
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, Mock
from .models import SystemModule

User = get_user_model()

class UserModelTestCase(TestCase):
    """用户模型测试"""

    def setUp(self):
        """测试前准备"""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """测试创建用户"""
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """测试创建超级用户"""
        user = User.objects.create_superuser(**self.user_data)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str_representation(self):
        """测试用户字符串表示"""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.email} ({user.username})"
        self.assertEqual(str(user), expected)

class UserAPITestCase(APITestCase):
    """用户API测试"""

    def setUp(self):
        """测试前准备"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )

    def test_user_login_success(self):
        """测试用户登录成功"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data['data'])
        self.assertIn('user', response.data['data'])

    def test_user_login_invalid_credentials(self):
        """测试无效凭据登录"""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/users/login/', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_get_user_profile_authenticated(self):
        """测试获取用户资料（已认证）"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], self.user.email)

    def test_get_user_profile_unauthenticated(self):
        """测试获取用户资料（未认证）"""
        response = self.client.get('/api/users/profile/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('plugins.dingtalk.DingTalkPlugin.get_user_info')
    def test_third_party_login(self, mock_get_user_info):
        """测试第三方登录"""
        # Mock第三方平台返回的用户信息
        mock_get_user_info.return_value = {
            'id': 'dingtalk_123',
            'name': '张三',
            'email': 'zhangsan@company.com',
            'avatar': 'https://example.com/avatar.jpg'
        }

        data = {
            'code': 'auth_code_123',
            'provider': 'dingtalk'
        }
        response = self.client.post('/api/users/third_party_login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

        # 验证用户是否创建
        user = User.objects.get(email='zhangsan@company.com')
        self.assertEqual(user.auth_source, 'dingtalk')
        self.assertEqual(user.external_id, 'dingtalk_123')
```

### 测试工厂

```python
import factory
from django.contrib.auth import get_user_model
from .models import SystemModule

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """用户工厂"""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_verified = False

class AdminUserFactory(UserFactory):
    """管理员用户工厂"""

    is_staff = True
    is_superuser = True
    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    username = factory.Sequence(lambda n: f"admin{n}")

class SystemModuleFactory(factory.django.DjangoModelFactory):
    """系统模块工厂"""

    class Meta:
        model = SystemModule

    name = factory.Sequence(lambda n: f"module_{n}")
    display_name = factory.Faker('word')
    description = factory.Faker('text')
    is_active = True
```

## 📝 日志规范

### 日志配置

```python
# utils/logger.py
import json
from typing import Any, Dict
from loguru import logger
from django.conf import settings

def get_logger():
    """获取配置好的logger实例"""

    # 移除默认handler
    logger.remove()

    # 添加控制台输出
    logger.add(
        sink=sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        level="INFO" if settings.DEBUG else "WARNING",
        colorize=True
    )

    # 添加文件输出
    logger.add(
        sink=settings.BASE_DIR / "logs" / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8"
    )

    return logger

# 使用示例
logger = get_logger()

def authenticate_user(email: str, password: str) -> Optional[User]:
    """用户认证"""
    logger.info("用户登录尝试", email=email, ip=get_client_ip())

    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            logger.info("用户登录成功", user_id=user.id, email=email)
            return user
        else:
            logger.warning("用户密码错误", email=email)
            return None
    except User.DoesNotExist:
        logger.warning("用户不存在", email=email)
        return None
    except Exception as e:
        logger.error("用户认证异常", email=email, error=str(e))
        return None
```

## 🔒 安全规范

### 敏感信息处理

```python
import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name: str, default: str = None) -> str:
    """获取环境变量"""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)

# settings.py
SECRET_KEY = get_env_variable('SECRET_KEY')
DATABASE_PASSWORD = get_env_variable('DB_PASSWORD')

# 敏感数据脱敏
def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """脱敏敏感数据"""
    sensitive_fields = ['password', 'token', 'secret', 'key']

    masked_data = data.copy()
    for field in sensitive_fields:
        if field in masked_data:
            value = str(masked_data[field])
            if len(value) > 4:
                masked_data[field] = value[:2] + '*' * (len(value) - 4) + value[-2:]
            else:
                masked_data[field] = '*' * len(value)

    return masked_data
```

### 输入验证

```python
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def validate_phone_number(phone: str) -> str:
    """验证手机号"""
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        raise ValidationError("手机号格式不正确")
    return phone

def validate_employee_id(employee_id: str) -> str:
    """验证工号"""
    if not employee_id.isalnum():
        raise ValidationError("工号只能包含字母和数字")
    if len(employee_id) < 3 or len(employee_id) > 20:
        raise ValidationError("工号长度必须在3-20位之间")
    return employee_id

# 在序列化器中使用
class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[validate_phone_number])
    employee_id = serializers.CharField(validators=[validate_employee_id])
```

## 🔗 相关文档

- [测试指南](testing.md) - 详细的测试方法和规范
- [部署指南](deployment.md) - 生产环境部署规范
- [API设计规范](api-design.md) - RESTful API设计原则
