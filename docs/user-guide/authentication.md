# 认证系统

## 📋 概述

Rookie 项目提供多种认证方式，支持传统的用户名密码登录、Token认证以及第三方平台扫码登录。

## 🔐 认证方式

### 1. Session认证 (Web页面)

#### 适用场景
- Web浏览器访问
- 管理后台操作
- 传统Web应用集成

#### 使用方法
```bash
# 访问登录页面
http://127.0.0.1:8000/login/

# 输入邮箱和密码登录
邮箱: admin@example.com
密码: password123
```

#### 特点
- ✅ 安全性高，Session存储在服务器
- ✅ 自动管理Cookie
- ✅ 支持CSRF保护
- ❌ 不适合移动端和API调用

### 2. Token认证 (API调用)

#### 适用场景
- API接口调用
- 移动应用开发
- 第三方系统集成
- 跨域访问

#### 获取Token
```bash
# 通过登录API获取Token
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'

# 响应包含Token
{
  "success": true,
  "data": {
    "user": {...},
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  }
}
```

#### 使用Token
```bash
# 在请求头中携带Token
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     http://127.0.0.1:8000/api/users/profile/
```

#### Token管理
```bash
# 获取当前Token信息
GET /api/users/get_token/

# 刷新Token
POST /api/users/refresh_token/

# 撤销Token
DELETE /api/users/revoke_token/
```

### 3. 第三方登录

#### 支持平台
- 📦 **钉钉**: 企业内部员工扫码登录
- 📱 **企业微信**: 企业成员快速登录
- 🐦 **飞书**: 团队协作平台登录
- 🐱 **GitHub**: 开源项目开发者登录

#### 配置步骤

##### 1. Admin后台配置
```bash
# 访问配置页面
http://127.0.0.1:8000/admin/users/thirdpartyauthconfig/

# 添加第三方认证配置
- 名称: dingtalk
- 显示名称: 钉钉登录
- 配置: JSON格式的配置信息
- 启用状态: 勾选
```

##### 2. 钉钉配置示例
```json
{
  "app_id": "dingoa123456789",
  "app_secret": "your_dingtalk_app_secret",
  "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/",
  "corp_id": "ding123456789"
}
```

##### 3. 企业微信配置示例
```json
{
  "corp_id": "ww123456789",
  "agent_id": "1000001",
  "secret": "your_wechat_work_secret",
  "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/"
}
```

#### 登录流程
```bash
# 1. 获取可用登录方式
GET /api/users/third_party_providers/

# 2. 跳转第三方登录
GET /api/users/third_party_auth/?provider=dingtalk

# 3. 用户扫码确认

# 4. 系统自动创建账户并登录
# 5. 返回用户信息和Token
```

## 👥 用户管理

### 用户注册

#### API注册
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "newuser",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

#### 第三方自动注册
- 组织内成员首次扫码登录时自动创建账户
- 同步第三方平台的用户信息
- 自动激活账户状态

### 用户信息管理

#### 获取用户信息
```bash
curl -H "Authorization: Token your_token" \
     http://127.0.0.1:8000/api/users/profile/
```

#### 更新用户资料
```bash
curl -X PATCH http://127.0.0.1:8000/api/users/update_profile/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "department": "技术部",
    "job_title": "高级工程师"
  }'
```

## 🔒 安全特性

### 密码安全
- 最小长度要求
- 复杂度验证
- 哈希存储
- 防暴力破解

### Token安全
- 随机生成40位字符串
- 服务器端存储和验证
- 支持主动撤销
- 无过期时间（可自定义）

### 第三方登录安全
- OAuth 2.0标准流程
- 状态参数防CSRF
- 回调地址验证
- 用户信息加密传输

## 🔧 配置选项

### 认证设置
```python
# settings/base.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# 登录设置
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/admin/'
```

### 第三方登录设置
```python
# 通过Admin后台配置
# 或使用初始化脚本
python examples/setup_third_party_auth.py
```

## 📊 使用统计

### 查看登录日志
```bash
# 查看日志文件
tail -f logs/dev.log | grep "登录成功"

# 或在Admin后台查看用户最后登录时间
```

### 用户活跃度
```bash
# 获取用户模块访问情况
curl -H "Authorization: Token your_token" \
     http://127.0.0.1:8000/api/users/my_modules/
```

## ❗ 常见问题

### Q: Token认证失败
**A**: 检查Token格式和有效性
```bash
# 确保使用正确格式
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# 不是Bearer格式
Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b  # ❌错误
```

### Q: 第三方登录配置无效
**A**: 检查配置参数和回调地址
```bash
# 确保回调地址与第三方平台配置一致
# 检查app_id、secret等参数正确性
# 确认第三方应用已审核通过
```

### Q: 用户权限不足
**A**: 检查用户组和权限分配
```bash
# 在Admin后台检查用户所属组
# 确认用户组有相应权限
# 检查权限检查代码是否正确
```

## 🔗 相关文档

- [权限管理](permissions.md) - 权限配置和使用
- [Token认证教程](../tutorials/token-auth-tutorial.md) - 详细实践教程
- [API参考](../api-reference/authentication.md) - 认证接口文档