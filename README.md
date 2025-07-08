# Rookie

一个开箱即用的 Django Web 应用项目模板，专为企业级应用设计。

## ✨ 特性

### 🏗️ 核心架构
- **Django 4.2+**: 基于最新稳定版本构建
- **开箱即用**: 预配置的项目结构和基本设置
- **环境隔离**: 支持开发/测试/生产环境配置
- **RESTful API**: 完整的API接口支持

### 📊 日志系统
- **Loguru集成**: 高性能、易用的日志库
- **多环境配置**: 不同环境的日志级别和输出方式
- **文件轮转**: 自动日志文件管理和压缩
- **结构化日志**: 支持上下文和结构化数据记录

### 👥 用户管理
- **自定义用户模型**: 基于邮箱登录的用户系统
- **用户资料扩展**: 灵活的用户信息管理
- **权限管理**: 基于Django的权限系统

### 🔐 开放式扫码登录
- **组织内登录**: 组织内所有人员都可扫码登录
- **自动注册**: 首次登录自动创建账户，同步组织信息
- **多平台支持**: 钉钉、企业微信、飞书等扫码登录
- **插件化架构**: 可扩展的第三方登录系统

### 🔑 模块权限系统
- **精细化权限**: 基于Django原生权限系统的模块级权限控制
- **用户组管理**: 支持用户和用户组两级权限分配
- **权限类型**: 支持查看/新增/修改/删除四种权限
- **动态授权**: 支持权限过期时间设置和动态管理

### 🎨 管理后台
- **Jazzmin美化**: 现代化的Admin界面
- **自定义Logo**: 支持品牌定制
- **响应式设计**: 适配各种设备
- **多主题支持**: 明暗主题切换

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/degary/RooKie.git
cd RooKie
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 初始化系统

```bash
# 创建超级用户
python manage.py createsuperuser

# 或使用演示数据
python examples/admin_demo.py

# 初始化系统模块和权限
python examples/setup_modules.py

# 配置第三方登录（可选）
python examples/setup_third_party_auth.py
```

### 5. 启动服务

```bash
# 开发环境（默认）
python manage.py runserver

# 指定环境
DJANGO_ENV=dev python manage.py runserver   # 开发环境
DJANGO_ENV=acc python manage.py runserver   # 测试环境
DJANGO_ENV=prod python manage.py runserver  # 生产环境
```

### 6. 访问应用

- **前台首页**: http://127.0.0.1:8000
- **Admin后台**: http://127.0.0.1:8000/admin/
- **API文档**: http://127.0.0.1:8000/api/

**默认登录信息:**
- 账号: admin@example.com
- 密码: password123

## 📊 日志系统

### 基本使用

```python
from utils.logger import get_logger

logger = get_logger()

# 基本日志
logger.info("这是信息日志")
logger.error("这是错误日志")

# 结构化日志
logger.info("用户操作", user_id=123, action="login")

# 异常记录
try:
    risky_operation()
except Exception:
    logger.exception("操作失败")
```

### 环境配置

```python
# 开发环境 - 控制台+文件输出
DJANGO_ENV=dev python manage.py runserver

# 测试环境 - 仅文件输出
DJANGO_ENV=acc python manage.py runserver

# 生产环境 - 仅文件输出，系统目录
DJANGO_ENV=prod python manage.py runserver
```

### 日志特性

- ✅ **高性能**: 基于 Loguru，性能优异
- ✅ **自动轮转**: 10MB 自动轮转和压缩
- ✅ **彩色输出**: 控制台彩色显示
- ✅ **结构化**: 支持上下文和结构化数据
- ✅ **错误分离**: 错误日志单独存储

### 示例代码

```bash
# 运行日志示例
python examples/logger_example.py

# 测试不同环境
python examples/simple_env_test.py
```

## 🔐 开放式扫码登录

### 支持平台

- 📦 **钉钉**: 组织内成员扫码登录，自动同步部门信息
- 📱 **企业微信**: 企业内成员扫码登录，自动同步组织架构
- 🐦 **飞书**: 企业内成员扫码登录，自动同步用户信息
- 🐱 **GitHub**: OAuth 登录（适用于开源团队）
- 🌐 **Google**: OAuth 登录（适用于企业邮箱）

### 登录特性

- ✅ **开放注册**: 组织内所有人员都可扫码登录
- ✅ **自动创建**: 首次登录自动创建账户，同步组织信息
- ✅ **信息同步**: 自动同步姓名、部门、职位、工号等
- ✅ **实时更新**: 组织架构变更时自动更新用户信息

### 配置步骤

#### 1. 初始化配置

```bash
# 创建默认配置
python examples/setup_third_party_auth.py
```

#### 2. Admin 后台配置

1. 访问 http://127.0.0.1:8000/admin/users/thirdpartyauthconfig/
2. 点击“增加第三方认证配置”
3. 按照页面提示填写配置

#### 3. 钉钉配置示例

```json
{
  "app_id": "dingoa123456789",
  "app_secret": "your_dingtalk_app_secret",
  "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/",
  "corp_id": "ding123456789"
}
```

### API 接口

```bash
# 获取可用登录方式
GET /api/users/third_party_providers/

# 第三方登录跳转
GET /api/users/third_party_auth/?provider=dingtalk

# 同步第三方用户
POST /api/users/sync_users/
```

### 扫码登录流程

1. **用户扫码**: 使用钉钉/企微等扫描登录二维码
2. **自动注册**: 系统自动创建账户，同步组织信息
3. **权限分配**: 管理员为用户分配模块访问权限
4. **模块访问**: 用户根据权限访问不同系统模块

## 🔑 模块权限系统

### 权限模型

基于Django原生权限系统，实现精细化的模块级权限控制：

```
系统模块 (SystemModule)
├── 👥 用户管理
├── ⚙️ 系统配置  
├── 📊 数据分析
├── 📁 文件管理
└── 🔔 消息通知

权限类型：
• can_view    - 可查看
• can_add     - 可新增  
• can_change  - 可修改
• can_delete  - 可删除
```

### 权限分配方式

#### **1. 用户组权限**
```python
# 默认用户组
managers    = [管理员]     # 用户管理 + 系统配置
analysts    = [数据分析师] # 数据分析 + 文件管理
employees   = [普通员工]   # 消息通知 + 文件查看
```

#### **2. 用户直接授权**
可为特定用户单独分配模块权限，优先级高于用户组权限。

### 权限检查使用

#### **装饰器方式**
```python
from utils.permissions import require_module_permission

@require_module_permission('user_management', 'view')
def user_list(request):
    # 只有有用户管理查看权限的用户才能访问
    pass
```

#### **类视图混入**
```python
from utils.permissions import ModulePermissionMixin

class UserListView(ModulePermissionMixin, ListView):
    module_name = 'user_management'
    permission_type = 'view'
```

#### **手动检查**
```python
from utils.permissions import permission_checker

if permission_checker.has_module_permission(user, 'data_analysis', 'view'):
    # 用户有数据分析查看权限
    pass
```

## 📁 项目结构

```
Rookie/
├── Rookie/                 # 项目配置
│   ├── settings/          # 分环境配置
│   │   ├── base.py        # 基础配置
│   │   ├── dev.py         # 开发环境
│   │   ├── acc.py         # 测试环境
│   │   └── prod.py        # 生产环境
│   └── urls.py            # 主路由配置
├── users/                 # 用户模块
│   ├── models.py          # 用户模型
│   ├── views.py           # 用户视图
│   ├── serializers.py     # API序列化器
│   ├── admin.py           # Admin配置
│   └── forms.py           # 表单定义
├── plugins/               # 第三方登录插件
│   ├── base.py            # 插件基类
│   ├── dingtalk.py        # 钉钉插件
│   ├── wechat_work.py     # 企业微信插件
│   └── manager.py         # 插件管理器
├── utils/                 # 工具模块
│   ├── logger.py          # 日志工具
│   └── permissions.py     # 权限检查工具
├── examples/              # 示例代码
│   ├── logger_example.py  # 日志示例
│   ├── admin_demo.py      # Admin演示数据
│   └── setup_third_party_auth.py # 第三方登录配置
├── static/                # 静态文件
│   └── images/            # 图片资源
├── logs/                  # 日志文件目录
├── manage.py              # Django管理命令
├── start_admin.py         # 一键启动脚本
└── requirements.txt       # 依赖列表
```

## 📡 API 文档

### 用户管理 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/users/register/` | 用户注册 |
| POST | `/api/users/login/` | 用户登录 |
| POST | `/api/users/logout/` | 用户登出 |
| GET | `/api/users/profile/` | 获取用户信息 |
| PUT | `/api/users/update_profile/` | 更新用户资料 |
| GET | `/api/users/my_modules/` | 获取用户可访问模块 |

### 扫码登录 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/users/third_party_providers/` | 获取可用扫码登录方式 |
| GET | `/api/users/third_party_auth/?provider=dingtalk` | 第三方登录跳转 |
| GET | `/api/users/third_party_callback/` | 第三方登录回调 |
| POST | `/api/users/sync_users/` | 同步组织用户 |

### 请求示例

```bash
# 用户注册
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "password_confirm": "password123"
  }'

# 获取扫码登录方式
curl http://127.0.0.1:8000/api/users/third_party_providers/

# 获取用户可访问模块
curl -H "Authorization: Bearer <token>" \
  http://127.0.0.1:8000/api/users/my_modules/
```

## 🚀 部署指南

### 开发环境

```bash
# 克隆代码
git clone https://github.com/degary/RooKie.git
cd RooKie

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python manage.py migrate

# 创建超级用户
python examples/admin_demo.py

# 启动服务
DJANGO_ENV=dev python manage.py runserver
```

### 生产环境

```bash
# 设置环境变量
export DJANGO_ENV=prod
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="your-database-url"

# 收集静态文件
python manage.py collectstatic --noinput

# 数据库迁移
python manage.py migrate

# 使用 Gunicorn 启动
gunicorn Rookie.wsgi:application --bind 0.0.0.0:8000
```

### Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "Rookie.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```bash
# 构建和运行
docker build -t rookie .
docker run -p 8000:8000 -e DJANGO_ENV=prod rookie
```

## 📋 函数返回规范

### 统一响应格式

所有API接口和函数调用都应使用统一的响应格式：

```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {...},
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "abc12345"
}
```

### 使用方式

#### API视图
```python
from utils.response import ApiResponse

# 成功响应
return ApiResponse.success(data=user_data).to_response()

# 错误响应
return ApiResponse.error("操作失败").to_response()
```

#### 普通函数
```python
from utils.response import ApiResponse

# 函数返回
def create_user(data):
    return ApiResponse.success(data=user_data)
```

#### 快捷方法
- `ApiResponse.success()` - 成功响应
- `ApiResponse.created()` - 创建成功
- `ApiResponse.error()` - 通用错误
- `ApiResponse.not_found()` - 资源不存在
- `ApiResponse.forbidden()` - 权限不足
- `ApiResponse.validation_error()` - 数据验证失败

详细使用方法请参考：[utils/response/README.md](utils/response/README.md)

## 🔧 开发指南

### 添加新的第三方登录插件

1. 在 `plugins/` 目录下创建新插件文件
2. 继承 `BaseAuthPlugin` 类
3. 实现必需的抽象方法
4. 在 `manager.py` 中注册插件

```python
# plugins/github.py
from .base import BaseAuthPlugin

class GitHubAuthPlugin(BaseAuthPlugin):
    @property
    def name(self) -> str:
        return 'github'
    
    @property
    def display_name(self) -> str:
        return 'GitHub'
    
    def get_auth_url(self) -> str:
        # 实现GitHub OAuth URL生成
        pass
    
    def get_user_info(self, code: str):
        # 实现用户信息获取
        pass
    
    def sync_users(self) -> int:
        # 实现用户同步（可选）
        return 0
```

### 自定义日志配置

在 `settings/` 中修改对应环境的 `LOGURU_CONFIG`：

```python
# settings/dev.py
LOGURU_CONFIG = {
    'console': {
        'enabled': True,
        'level': 'DEBUG',  # 开发环境显示所有日志
    },
    'file': {
        'enabled': True,
        'level': 'INFO',
        'path': BASE_DIR / 'logs' / 'dev.log',
    }
}
```

## 📚 参考资料

- [Django 官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Loguru 文档](https://loguru.readthedocs.io/)
- [Jazzmin 文档](https://django-jazzmin.readthedocs.io/)
- [钉钉开放平台](https://open.dingtalk.com/)
- [企业微信开发文档](https://developer.work.weixin.qq.com/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- ✨ 基础Django项目结构
- ✨ Loguru日志系统集成
- ✨ 自定义用户模型
- ✨ Jazzmin Admin后台美化
- ✨ 第三方登录插件系统
- ✨ 钉钉和企业微信登录支持
- ✨ RESTful API 接口

## ⚖️ 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件