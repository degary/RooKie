# 快速开始

## 📋 概述

本文档帮助您在5分钟内启动 Rookie 项目并体验核心功能。

## 🚀 5分钟快速体验

### 前置条件
- 已完成 [安装部署](installation.md)
- Python 虚拟环境已激活

### 1. 启动项目 (1分钟)

```bash
# 进入项目目录
cd RooKie

# 启动开发服务器
python manage.py runserver
```

**预期输出:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 01, 2024 - 12:00:00
Django version 4.2.0, using settings 'Rookie.settings.dev'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 2. 访问应用 (1分钟)

#### 登录页面
- **地址**: http://127.0.0.1:8000/login/
- **功能**: 支持账号登录和扫码登录

#### 管理后台
- **地址**: http://127.0.0.1:8000/admin/
- **默认账号**: admin@example.com
- **默认密码**: password123

### 3. 体验功能 (3分钟)

#### 用户登录
```bash
# 使用curl测试登录API
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

**预期响应:**
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1,
      "email": "admin@example.com",
      "username": "admin"
    },
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
  }
}
```

#### 获取用户信息
```bash
# 使用Token访问API (替换为实际Token)
export TOKEN="a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"

curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/
```

#### 查看用户权限
```bash
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/my_modules/
```

## 🎯 核心功能演示

### 1. 认证系统

#### Session认证 (Web页面)
- 访问登录页面进行登录
- 登录后可访问管理后台

#### Token认证 (API调用)
- 通过登录API获取Token
- 使用Token调用其他API接口

### 2. 权限管理

#### 查看权限配置
1. 访问 http://127.0.0.1:8000/admin/
2. 进入 `用户管理 > 系统模块`
3. 查看已配置的功能模块

#### 用户组管理
1. 进入 `权限管理 > 用户组`
2. 查看默认用户组和权限分配

### 3. 第三方登录

#### 查看可用登录方式
```bash
curl http://127.0.0.1:8000/api/users/third_party_providers/
```

#### 配置第三方登录
1. 访问 http://127.0.0.1:8000/admin/users/thirdpartyauthconfig/
2. 添加钉钉、企微等登录配置

## 📊 项目结构概览

```
RooKie/
├── Rookie/                 # 项目配置
│   ├── settings/          # 分环境配置
│   └── urls.py            # 主路由
├── users/                 # 用户模块
│   ├── models.py          # 用户模型
│   ├── views.py           # API视图
│   └── admin.py           # Admin配置
├── utils/                 # 工具模块
│   ├── response/          # 响应包装器
│   └── auth/              # 权限工具
├── templates/             # 模板文件
│   └── auth/              # 认证页面
├── docs/                  # 项目文档
└── examples/              # 示例脚本
```

## 🔧 开发环境配置

### 环境变量
```bash
# 开发环境 (默认)
export DJANGO_ENV=dev

# 测试环境
export DJANGO_ENV=acc

# 生产环境
export DJANGO_ENV=prod
export SECRET_KEY="your-secret-key"
```

### 日志配置
```bash
# 查看日志文件
ls logs/

# 实时查看日志
tail -f logs/dev.log
```

### 数据库管理
```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations
```

## ✅ 验证清单

完成快速开始后，请确认以下功能正常：

- [ ] 项目成功启动，无错误信息
- [ ] 可以访问登录页面
- [ ] 可以登录管理后台
- [ ] API接口返回正确响应
- [ ] Token认证工作正常
- [ ] 权限系统配置正确

## 🚨 常见问题

### Q: 服务器启动失败
```bash
# 检查端口占用
lsof -i :8000

# 使用其他端口
python manage.py runserver 8001
```

### Q: 登录失败
```bash
# 重新创建超级用户
python manage.py createsuperuser

# 或使用演示数据
python examples/admin_demo.py
```

### Q: API返回401错误
```bash
# 检查Token是否正确
echo $TOKEN

# 重新获取Token
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'
```

## 🔗 下一步

快速体验完成后，建议继续学习：

- [第一个API](first-api.md) - 详细的API调用示例
- [认证系统](../user-guide/authentication.md) - 深入了解认证机制
- [权限管理](../user-guide/permissions.md) - 权限配置和使用
- [API参考](../api-reference/README.md) - 完整的API文档