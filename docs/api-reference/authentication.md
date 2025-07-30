# 认证接口

## 📋 概述

认证接口提供用户登录、注册、Token管理和第三方登录等功能。

## 🔐 用户认证

### 用户注册

**接口地址**: `POST /api/users/register/`
**认证要求**: 无
**权限要求**: 无

#### 请求参数
```json
{
  "email": "user@example.com",        // 必填，邮箱地址
  "username": "newuser",              // 必填，用户名
  "password": "password123",          // 必填，密码
  "password_confirm": "password123",  // 必填，确认密码
  "phone": "13800138000",            // 可选，手机号
  "department": "技术部",             // 可选，部门
  "job_title": "工程师"               // 可选，职位
}
```

#### 响应示例
```json
{
  "success": true,
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 2,
      "email": "user@example.com",
      "username": "newuser",
      "phone": "13800138000",
      "department": "技术部",
      "job_title": "工程师",
      "is_active": true,
      "date_joined": "2024-01-01T12:00:00Z"
    }
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "abc12345"
}
```

#### 错误响应
```json
{
  "success": false,
  "code": 422,
  "message": "数据验证失败",
  "data": {
    "email": ["邮箱格式不正确"],
    "password": ["密码长度至少8位"]
  }
}
```

### 用户登录

**接口地址**: `POST /api/users/login/`
**认证要求**: 无
**权限要求**: 无

#### 请求参数
```json
{
  "email": "user@example.com",    // 必填，邮箱地址
  "password": "password123"       // 必填，密码
}
```

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 2,
      "email": "user@example.com",
      "username": "newuser",
      "phone": "13800138000",
      "department": "技术部",
      "job_title": "工程师",
      "is_active": true,
      "is_superuser": false,
      "last_login": "2024-01-01T12:00:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  }
}
```

### 用户登出

**接口地址**: `POST /api/users/logout/`
**认证要求**: Token或Session
**权限要求**: 已登录用户

#### 请求参数
无

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "登出成功"
}
```

## 🔑 Token管理

### 获取Token信息

**接口地址**: `GET /api/users/get_token/`
**认证要求**: Token或Session
**权限要求**: 已登录用户

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "Token获取成功",
  "data": {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

### 刷新Token

**接口地址**: `POST /api/users/refresh_token/`
**认证要求**: Token或Session
**权限要求**: 已登录用户

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "Token刷新成功",
  "data": {
    "token": "新的token字符串"
  }
}
```

### 撤销Token

**接口地址**: `DELETE /api/users/revoke_token/`
**认证要求**: Token或Session
**权限要求**: 已登录用户

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "Token已撤销",
  "data": {
    "deleted_count": 1
  }
}
```

## 🌐 第三方登录

### 获取登录提供商

**接口地址**: `GET /api/users/third_party_providers/`
**认证要求**: 无
**权限要求**: 无

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "获取登录方式成功",
  "data": {
    "providers": [
      {
        "name": "dingtalk",
        "display_name": "钉钉登录",
        "auth_url": "https://oapi.dingtalk.com/connect/oauth2/sns_authorize?appid=xxx&response_type=code&scope=snsapi_login&state=dingtalk_login&redirect_uri=xxx"
      },
      {
        "name": "wechat_work",
        "display_name": "企业微信登录",
        "auth_url": "https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=xxx&agentid=xxx&redirect_uri=xxx&state=wechat_work_login"
      }
    ]
  }
}
```

### 第三方登录跳转

**接口地址**: `GET /api/users/third_party_auth/`
**认证要求**: 无
**权限要求**: 无

#### 请求参数
```
provider: 登录提供商名称 (dingtalk, wechat_work, feishu等)
```

#### 响应
自动跳转到第三方登录页面

### 第三方登录回调

**接口地址**: `GET /api/users/third_party_callback/`
**认证要求**: 无
**权限要求**: 无

#### 请求参数
```
code: 第三方平台返回的授权码
state: 状态参数
```

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 3,
      "email": "user@dingtalk.local",
      "username": "张三",
      "phone": "13800138000",
      "department": "技术部",
      "job_title": "高级工程师",
      "employee_id": "E001",
      "auth_source": "dingtalk",
      "external_id": "dingtalk_user_123",
      "is_active": true
    },
    "token": "新用户的token字符串"
  }
}
```

### 同步第三方用户

**接口地址**: `POST /api/users/sync_users/`
**认证要求**: Token或Session
**权限要求**: 管理员权限

#### 请求参数
```json
{
  "provider": "dingtalk"    // 必填，第三方平台名称
}
```

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "同步完成，共同步 15 个用户",
  "data": {
    "count": 15
  }
}
```

## 🔧 使用示例

### JavaScript示例
```javascript
// 用户登录
async function login(email, password) {
  const response = await fetch('/api/users/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  const result = await response.json();

  if (result.success) {
    // 保存Token
    localStorage.setItem('auth_token', result.data.token);
    return result.data.user;
  } else {
    throw new Error(result.message);
  }
}

// 使用Token调用API
async function apiCall(endpoint, options = {}) {
  const token = localStorage.getItem('auth_token');

  const response = await fetch(`/api${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`,
      ...options.headers
    }
  });

  return response.json();
}
```

### Python示例
```python
import requests

class AuthAPI:
    def __init__(self, base_url="http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()

    def login(self, email, password):
        """用户登录"""
        response = self.session.post(
            f"{self.base_url}/users/login/",
            json={"email": email, "password": password}
        )
        result = response.json()

        if result['success']:
            self.token = result['data']['token']
            self.session.headers.update({
                'Authorization': f'Token {self.token}'
            })
            return result['data']['user']
        else:
            raise Exception(result['message'])

    def get_token_info(self):
        """获取Token信息"""
        response = self.session.get(f"{self.base_url}/users/get_token/")
        result = response.json()

        if result['success']:
            return result['data']
        else:
            raise Exception(result['message'])

    def refresh_token(self):
        """刷新Token"""
        response = self.session.post(f"{self.base_url}/users/refresh_token/")
        result = response.json()

        if result['success']:
            self.token = result['data']['token']
            self.session.headers.update({
                'Authorization': f'Token {self.token}'
            })
            return self.token
        else:
            raise Exception(result['message'])

# 使用示例
auth = AuthAPI()
user = auth.login('user@example.com', 'password123')
print(f"登录成功: {user['email']}")
```

## 🚨 错误处理

### 常见错误

#### 登录失败
```json
{
  "success": false,
  "code": 422,
  "message": "登录信息验证失败",
  "data": {
    "non_field_errors": ["邮箱或密码错误"]
  }
}
```

#### Token无效
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问"
}
```

#### 第三方登录失败
```json
{
  "success": false,
  "code": 400,
  "message": "获取用户信息失败"
}
```

## 🔗 相关文档

- [用户接口](users.md) - 用户信息管理
- [权限接口](permissions.md) - 权限相关接口
- [响应格式](responses.md) - 统一响应格式说明
