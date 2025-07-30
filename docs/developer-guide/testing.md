# 测试指南

## 📋 概述

本文档介绍 Rookie 项目的测试策略、测试方法和最佳实践。

## 🧪 测试策略

### 测试金字塔

```
    /\
   /  \     E2E Tests (端到端测试)
  /____\    Integration Tests (集成测试)
 /______\   Unit Tests (单元测试)
```

- **单元测试 (70%)**: 测试单个函数、方法、类
- **集成测试 (20%)**: 测试模块间交互
- **端到端测试 (10%)**: 测试完整用户流程

### 测试分类

#### 1. 单元测试
- 模型测试
- 工具函数测试
- 序列化器测试
- 权限检查测试

#### 2. 集成测试
- API接口测试
- 数据库操作测试
- 第三方服务集成测试

#### 3. 功能测试
- 用户认证流程测试
- 权限系统测试
- 业务流程测试

## 🛠️ 测试工具

### 核心工具
- **pytest**: 测试框架
- **pytest-django**: Django集成
- **factory-boy**: 测试数据工厂
- **coverage**: 覆盖率统计
- **requests-mock**: HTTP请求模拟

### 安装测试依赖

```bash
pip install -r requirements-dev.txt
```

## 📁 测试结构

```
tests/
├── __init__.py
├── conftest.py              # pytest配置
├── factories.py             # 测试数据工厂
├── unit/                    # 单元测试
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_serializers.py
│   ├── test_utils.py
│   └── test_permissions.py
├── integration/             # 集成测试
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_auth.py
│   └── test_third_party.py
├── functional/              # 功能测试
│   ├── __init__.py
│   ├── test_user_flow.py
│   └── test_admin_flow.py
└── fixtures/                # 测试数据
    ├── users.json
    └── modules.json
```#
# 🏭 测试工厂

### 基础工厂

```python
# tests/factories.py
import factory
from django.contrib.auth import get_user_model
from users.models import SystemModule, ThirdPartyAuthConfig

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """用户工厂"""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone = factory.Faker('phone_number')
    is_active = True
    is_verified = False

class AdminUserFactory(UserFactory):
    """管理员工厂"""
    is_staff = True
    is_superuser = True

class SystemModuleFactory(factory.django.DjangoModelFactory):
    """系统模块工厂"""

    class Meta:
        model = SystemModule

    name = factory.Sequence(lambda n: f"module_{n}")
    display_name = factory.Faker('word')
    description = factory.Faker('text')
    is_active = True
```

### 使用工厂

```python
# 创建单个对象
user = UserFactory()
admin = AdminUserFactory()

# 创建多个对象
users = UserFactory.create_batch(5)

# 自定义属性
user = UserFactory(email='custom@example.com')

# 构建对象（不保存到数据库）
user = UserFactory.build()
```

## 🧪 单元测试

### 模型测试

```python
# tests/unit/test_models.py
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from tests.factories import UserFactory, SystemModuleFactory

User = get_user_model()

class UserModelTestCase(TestCase):
    """用户模型测试"""

    def test_create_user(self):
        """测试创建用户"""
        user = UserFactory()

        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_user_str_representation(self):
        """测试用户字符串表示"""
        user = UserFactory(
            email='test@example.com',
            first_name='张',
            last_name='三'
        )
        expected = "test@example.com (张三)"
        self.assertEqual(str(user), expected)

    def test_get_display_name(self):
        """测试获取显示名称"""
        # 有全名的情况
        user = UserFactory(first_name='张', last_name='三')
        self.assertEqual(user.get_display_name(), '张三')

        # 只有用户名的情况
        user = UserFactory(first_name='', last_name='', username='testuser')
        self.assertEqual(user.get_display_name(), 'testuser')

    def test_has_module_permission_superuser(self):
        """测试超级用户权限"""
        admin = AdminUserFactory()
        self.assertTrue(admin.has_module_permission('any_module', 'any_action'))

    def test_email_uniqueness(self):
        """测试邮箱唯一性"""
        UserFactory(email='test@example.com')

        with self.assertRaises(Exception):
            UserFactory(email='test@example.com')
```

### 序列化器测试

```python
# tests/unit/test_serializers.py
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.serializers import UserSerializer, LoginSerializer
from tests.factories import UserFactory

class UserSerializerTestCase(TestCase):
    """用户序列化器测试"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

    def test_user_serialization(self):
        """测试用户序列化"""
        serializer = UserSerializer(self.user)
        data = serializer.data

        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['username'], self.user.username)
        self.assertIn('full_name', data)
        self.assertIn('permissions', data)

    def test_user_deserialization(self):
        """测试用户反序列化"""
        data = {
            'email': 'new@example.com',
            'username': 'newuser',
            'first_name': '新',
            'last_name': '用户'
        }
        serializer = UserSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, data['email'])

class LoginSerializerTestCase(TestCase):
    """登录序列化器测试"""

    def setUp(self):
        self.user = UserFactory(email='test@example.com')
        self.user.set_password('testpass123')
        self.user.save()

    def test_valid_login_data(self):
        """测试有效登录数据"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        """测试无效邮箱"""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpass123'
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
```

## 🔗 集成测试

### API测试

```python
# tests/integration/test_api.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from tests.factories import UserFactory, AdminUserFactory

class UserAPITestCase(TestCase):
    """用户API测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.admin = AdminUserFactory()
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)

    def test_login_success(self):
        """测试登录成功"""
        self.user.set_password('testpass123')
        self.user.save()

        data = {
            'email': self.user.email,
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data['data'])

    def test_login_invalid_credentials(self):
        """测试无效凭据登录"""
        data = {
            'email': self.user.email,
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/users/login/', data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])

    def test_get_profile_authenticated(self):
        """测试获取用户资料（已认证）"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get('/api/users/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], self.user.email)

    def test_get_profile_unauthenticated(self):
        """测试获取用户资料（未认证）"""
        response = self.client.get('/api/users/profile/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_admin_only(self):
        """测试用户列表（仅管理员）"""
        # 普通用户访问
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 管理员访问
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### 第三方登录测试

```python
# tests/integration/test_third_party.py
from unittest.mock import patch, Mock
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import ThirdPartyAuthConfig

class ThirdPartyLoginTestCase(TestCase):
    """第三方登录测试"""

    def setUp(self):
        self.client = APIClient()

        # 创建钉钉配置
        self.dingtalk_config = ThirdPartyAuthConfig.objects.create(
            name='dingtalk',
            display_name='钉钉',
            config={
                'app_id': 'test_app_id',
                'app_secret': 'test_app_secret',
                'redirect_uri': 'http://localhost:8000/api/auth/dingtalk/callback/'
            },
            is_enabled=True
        )

    @patch('plugins.dingtalk.DingTalkPlugin.get_user_info')
    def test_dingtalk_login_new_user(self, mock_get_user_info):
        """测试钉钉登录（新用户）"""
        # Mock钉钉返回的用户信息
        mock_get_user_info.return_value = {
            'id': 'dingtalk_123',
            'name': '张三',
            'email': 'zhangsan@company.com',
            'avatar': 'https://example.com/avatar.jpg',
            'mobile': '13800138000'
        }

        data = {
            'code': 'auth_code_123',
            'provider': 'dingtalk'
        }
        response = self.client.post('/api/users/third_party_login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data['data'])

        # 验证用户创建
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(email='zhangsan@company.com')
        self.assertEqual(user.auth_source, 'dingtalk')
        self.assertEqual(user.external_id, 'dingtalk_123')

    @patch('plugins.dingtalk.DingTalkPlugin.get_user_info')
    def test_dingtalk_login_existing_user(self, mock_get_user_info):
        """测试钉钉登录（已存在用户）"""
        # 创建已存在的用户
        from tests.factories import UserFactory
        existing_user = UserFactory(
            email='zhangsan@company.com',
            auth_source='dingtalk',
            external_id='dingtalk_123'
        )

        mock_get_user_info.return_value = {
            'id': 'dingtalk_123',
            'name': '张三',
            'email': 'zhangsan@company.com'
        }

        data = {
            'code': 'auth_code_123',
            'provider': 'dingtalk'
        }
        response = self.client.post('/api/users/third_party_login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

        # 验证没有创建新用户
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.assertEqual(User.objects.filter(email='zhangsan@company.com').count(), 1)

    @patch('plugins.dingtalk.DingTalkPlugin.get_user_info')
    def test_dingtalk_login_api_error(self, mock_get_user_info):
        """测试钉钉API错误"""
        mock_get_user_info.side_effect = Exception("API调用失败")

        data = {
            'code': 'auth_code_123',
            'provider': 'dingtalk'
        }
        response = self.client.post('/api/users/third_party_login/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
```

## 🎭 功能测试

### 用户流程测试

```python
# tests/functional/test_user_flow.py
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import UserFactory

class UserFlowTestCase(TransactionTestCase):
    """用户完整流程测试"""

    def setUp(self):
        self.client = APIClient()

    def test_complete_user_registration_and_login_flow(self):
        """测试完整的用户注册和登录流程"""
        # 1. 用户注册
        register_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123',
            'first_name': '新',
            'last_name': '用户'
        }
        response = self.client.post('/api/users/register/', register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. 用户登录
        login_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/users/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['data']['token']

        # 3. 获取用户资料
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'newuser@example.com')

        # 4. 更新用户资料
        update_data = {
            'phone': '13800138000',
            'department': '技术部'
        }
        response = self.client.patch('/api/users/profile/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 5. 修改密码
        password_data = {
            'old_password': 'newpass123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456'
        }
        response = self.client.post('/api/users/change_password/', password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 6. 使用新密码登录
        self.client.credentials()  # 清除认证
        login_data['password'] = 'newpass456'
        response = self.client.post('/api/users/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

## 📊 测试覆盖率

### 配置覆盖率

```python
# .coveragerc
[run]
source = .
omit =
    */venv/*
    */migrations/*
    */tests/*
    manage.py
    */settings/*
    */wsgi.py
    */asgi.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### 运行覆盖率测试

```bash
# 运行测试并生成覆盖率报告
coverage run --source='.' manage.py test
coverage report
coverage html

# 查看HTML报告
open htmlcov/index.html
```

## 🚀 运行测试

### 基本命令

```bash
# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test users

# 运行特定测试类
python manage.py test users.tests.test_models.UserModelTestCase

# 运行特定测试方法
python manage.py test users.tests.test_models.UserModelTestCase.test_create_user
```

### 使用pytest

```bash
# 运行所有测试
pytest

# 运行特定目录
pytest tests/unit/

# 运行特定文件
pytest tests/unit/test_models.py

# 运行特定测试
pytest tests/unit/test_models.py::UserModelTestCase::test_create_user

# 显示详细输出
pytest -v

# 显示print输出
pytest -s

# 并行运行测试
pytest -n auto
```

### 测试配置

```python
# pytest.ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = Rookie.settings.test
python_files = tests.py test_*.py *_tests.py
python_classes = Test* *Tests *TestCase
python_functions = test_*
addopts =
    --tb=short
    --strict-markers
    --disable-warnings
    --reuse-db
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

## 🔧 测试最佳实践

### 1. 测试命名

```python
# 好的测试命名
def test_user_login_with_valid_credentials_returns_token(self):
    pass

def test_user_login_with_invalid_password_returns_error(self):
    pass

# 不好的测试命名
def test_login(self):
    pass

def test_user_stuff(self):
    pass
```

### 2. 测试结构

```python
def test_something(self):
    # Arrange (准备)
    user = UserFactory()
    data = {'email': user.email, 'password': 'test123'}

    # Act (执行)
    response = self.client.post('/api/users/login/', data)

    # Assert (断言)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data['success'])
```

### 3. 使用Mock

```python
from unittest.mock import patch, Mock

@patch('users.services.send_email')
def test_user_registration_sends_welcome_email(self, mock_send_email):
    """测试用户注册发送欢迎邮件"""
    data = {'email': 'test@example.com', 'password': 'test123'}
    response = self.client.post('/api/users/register/', data)

    self.assertEqual(response.status_code, 201)
    mock_send_email.assert_called_once_with(
        to='test@example.com',
        subject='欢迎注册'
    )
```

### 4. 测试数据隔离

```python
from django.test import TransactionTestCase

class DatabaseTestCase(TransactionTestCase):
    """需要真实数据库事务的测试"""

    def test_concurrent_user_creation(self):
        # 测试并发用户创建
        pass
```

## 🔗 相关文档

- [编码规范](coding-standards.md) - 代码质量标准
- [部署指南](deployment.md) - 生产环境测试
- [API参考](../api-reference/README.md) - API接口文档
