# 常见问题

## 📋 概述

本文档收集了 Rookie 项目使用过程中的常见问题和解决方案。

## 🚀 安装启动问题

### Q: pip install 失败
**现象**: 安装依赖时出现错误
```bash
ERROR: Could not find a version that satisfies the requirement...
```

**解决方案**:
```bash
# 1. 升级pip
pip install --upgrade pip

# 2. 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 3. 检查Python版本
python --version  # 确保是3.8+
```

### Q: 数据库迁移失败
**现象**: 运行migrate命令时出错
```bash
django.db.utils.OperationalError: no such table: django_migrations
```

**解决方案**:
```bash
# 1. 删除迁移文件
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 2. 重新创建迁移
python manage.py makemigrations
python manage.py migrate

# 3. 如果仍有问题，删除数据库文件
rm db.sqlite3
python manage.py migrate
```

### Q: 服务器启动失败
**现象**: runserver命令无法启动
```bash
Error: That port is already in use.
```

**解决方案**:
```bash
# 1. 查看端口占用
lsof -i :8000

# 2. 杀死占用进程
kill -9 <PID>

# 3. 使用其他端口
python manage.py runserver 8001

# 4. 检查防火墙设置
sudo ufw status
```

### Q: 模块导入错误
**现象**: 启动时提示模块不存在
```bash
ModuleNotFoundError: No module named 'simpleui'
```

**解决方案**:
```bash
# 1. 确认虚拟环境已激活
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. 重新安装依赖
pip install -r requirements.txt

# 3. 检查PYTHONPATH
echo $PYTHONPATH
```

## 🔐 认证权限问题

### Q: 登录失败
**现象**: 使用正确的邮箱密码仍无法登录
```json
{
  "success": false,
  "message": "登录信息验证失败"
}
```

**解决方案**:
```bash
# 1. 检查用户是否存在
python manage.py shell
>>> from users.models import User
>>> User.objects.filter(email='admin@example.com').exists()

# 2. 重置用户密码
python manage.py changepassword admin@example.com

# 3. 创建新的超级用户
python manage.py createsuperuser

# 4. 使用演示数据
python examples/admin_demo.py
```

### Q: Token认证失败
**现象**: API调用返回401错误
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问"
}
```

**解决方案**:
```bash
# 1. 检查Token格式
# 正确格式: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
# 错误格式: Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# 2. 重新获取Token
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'

# 3. 检查Token是否存在
python manage.py shell
>>> from rest_framework.authtoken.models import Token
>>> Token.objects.all()

# 4. 为用户创建Token
>>> from users.models import User
>>> user = User.objects.get(email='admin@example.com')
>>> token, created = Token.objects.get_or_create(user=user)
>>> print(token.key)
```

### Q: 权限不足
**现象**: API调用返回403错误
```json
{
  "success": false,
  "code": 403,
  "message": "权限不足"
}
```

**解决方案**:
```bash
# 1. 检查用户权限
curl -H "Authorization: Token your_token" \
     http://127.0.0.1:8000/api/users/my_modules/

# 2. 在Admin后台分配权限
# 访问: http://127.0.0.1:8000/admin/auth/group/
# 将用户添加到相应的用户组

# 3. 直接为用户分配权限
python manage.py shell
>>> from users.models import User
>>> from django.contrib.auth.models import Permission
>>> user = User.objects.get(email='user@example.com')
>>> permission = Permission.objects.get(codename='view_systemmodule')
>>> user.user_permissions.add(permission)

# 4. 初始化权限系统
python examples/setup_permissions.py
```

### Q: 第三方登录失败
**现象**: 扫码登录后无法正常登录
```json
{
  "success": false,
  "message": "获取用户信息失败"
}
```

**解决方案**:
```bash
# 1. 检查第三方配置
# 访问: http://127.0.0.1:8000/admin/users/thirdpartyauthconfig/
# 确认配置信息正确

# 2. 验证回调地址
# 确保redirect_uri与第三方平台配置一致
# 检查域名和端口是否正确

# 3. 检查应用权限
# 确认第三方应用已获得必要的权限
# 检查应用审核状态

# 4. 查看详细错误日志
tail -f logs/dev.log | grep "第三方登录"
```

## 🌐 API调用问题

### Q: CORS跨域错误
**现象**: 前端调用API时出现跨域错误
```
Access to fetch at 'http://127.0.0.1:8000/api/' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**解决方案**:
```bash
# 1. 安装django-cors-headers
pip install django-cors-headers

# 2. 配置settings.py
INSTALLED_APPS = [
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# 3. 开发环境允许所有域名
CORS_ALLOW_ALL_ORIGINS = True  # 仅开发环境
```

### Q: 请求超时
**现象**: API请求长时间无响应
```
TimeoutError: Request timed out
```

**解决方案**:
```bash
# 1. 检查服务器状态
curl -I http://127.0.0.1:8000/api/users/third_party_providers/

# 2. 增加超时时间
# JavaScript
fetch('/api/users/profile/', {
  signal: AbortSignal.timeout(30000)  // 30秒超时
})

# Python
import requests
response = requests.get('/api/users/profile/', timeout=30)

# 3. 检查数据库连接
python manage.py dbshell

# 4. 查看服务器负载
top
htop
```

### Q: 数据格式错误
**现象**: API返回数据格式不正确
```json
{
  "detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"
}
```

**解决方案**:
```bash
# 1. 检查Content-Type
curl -H "Content-Type: application/json" \
     -d '{"email": "user@example.com"}' \
     http://127.0.0.1:8000/api/users/login/

# 2. 验证JSON格式
echo '{"email": "user@example.com"}' | python -m json.tool

# 3. 检查字符编码
# 确保使用UTF-8编码

# 4. 查看原始响应
curl -v http://127.0.0.1:8000/api/users/profile/
```

## 🔧 配置部署问题

### Q: 静态文件无法加载
**现象**: Admin后台样式丢失
```
GET /static/admin/css/base.css 404 (Not Found)
```

**解决方案**:
```bash
# 1. 收集静态文件
python manage.py collectstatic

# 2. 检查静态文件配置
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 3. 开发环境配置URL
# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Q: 环境变量不生效
**现象**: 设置的环境变量无法读取
```bash
KeyError: 'DJANGO_ENV'
```

**解决方案**:
```bash
# 1. 检查环境变量设置
echo $DJANGO_ENV

# 2. 在当前shell中设置
export DJANGO_ENV=dev

# 3. 永久设置环境变量
# ~/.bashrc 或 ~/.zshrc
echo 'export DJANGO_ENV=dev' >> ~/.bashrc
source ~/.bashrc

# 4. 使用.env文件
pip install python-dotenv

# .env文件
DJANGO_ENV=dev
SECRET_KEY=your-secret-key

# settings.py
from dotenv import load_dotenv
load_dotenv()
```

### Q: 数据库连接池耗尽
**现象**: 生产环境数据库连接失败
```
django.db.utils.OperationalError: FATAL: remaining connection slots are reserved
```

**解决方案**:
```bash
# 1. 配置数据库连接池
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        }
    }
}

# 2. 使用连接池中间件
pip install django-db-connection-pool

# 3. 检查数据库连接数
# PostgreSQL
SELECT count(*) FROM pg_stat_activity;

# 4. 优化查询
# 使用select_related和prefetch_related
# 避免N+1查询问题
```

## 🔍 调试技巧

### 启用调试模式
```python
# settings/dev.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### 使用Django Shell调试
```bash
python manage.py shell

# 测试模型
>>> from users.models import User
>>> User.objects.all()

# 测试权限
>>> from utils.auth.permissions import permission_checker
>>> user = User.objects.first()
>>> permission_checker.has_module_permission(user, 'user_management', 'view')

# 测试API
>>> from django.test import Client
>>> client = Client()
>>> response = client.post('/api/users/login/', {'email': 'admin@example.com', 'password': 'password123'})
>>> response.json()
```

### 查看SQL查询
```python
# settings.py
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

# 或在代码中
from django.db import connection
print(connection.queries)
```

## 🔗 相关文档

- [错误码说明](error-codes.md) - 详细错误码含义
- [调试指南](debugging.md) - 系统调试方法
- [用户指南](../user-guide/README.md) - 功能使用说明
