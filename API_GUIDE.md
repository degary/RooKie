# Rookie API 使用指南

## 📖 概述

Rookie 提供了完整的 RESTful API，支持用户管理、认证授权、第三方登录等功能。所有 API 都遵循统一的响应格式，并提供详细的错误信息。

## 🔗 基础信息

- **Base URL**: `http://your-domain.com/api/`
- **API版本**: v1
- **内容类型**: `application/json`
- **字符编码**: UTF-8

## 🔐 认证方式

### Token 认证（推荐）

```bash
# 请求头格式
Authorization: Token your-token-here
```

### Session 认证

```bash
# 使用 Cookie 进行认证
Cookie: sessionid=your-session-id
```

## 📊 统一响应格式

### 成功响应

```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {
    // 具体数据
  },
  "timestamp": "2024-01-01T00:00:00Z",
  "request_id": "abc12345"
}
```

### 错误响应

```json
{
  "success": false,
  "code": 400,
  "message": "请求参数错误",
  "errors": {
    "field_name": ["错误详情"]
  },
  "timestamp": "2024-01-01T00:00:00Z",
  "request_id": "abc12345"
}
```

### HTTP 状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证或认证失败 |
| 403 | Forbidden | 权限不足 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

## 👥 用户管理 API

### 用户注册

**POST** `/api/users/register/`

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "newuser",
    "password": "securepassword123",
    "phone": "13800138000"
  }'
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| email | string | ✅ | 邮箱地址，用作登录名 |
| username | string | ✅ | 用户名，3-30个字符 |
| password | string | ✅ | 密码，至少8个字符 |
| phone | string | ❌ | 手机号码 |

**响应示例**:
```json
{
  "success": true,
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "user@example.com",
      "username": "newuser",
      "phone": "13800138000",
      "is_verified": false,
      "created_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 用户登录

**POST** `/api/users/login/`

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| email | string | ✅ | 邮箱地址 |
| password | string | ✅ | 密码 |

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "admin@example.com",
      "username": "admin",
      "is_staff": true,
      "is_superuser": true
    },
    "token": "your-token-here"
  }
}
```

### 获取用户信息

**GET** `/api/users/profile/`

```bash
curl -H "Authorization: Token your-token-here" \
     http://127.0.0.1:8000/api/users/profile/
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "获取用户信息成功",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "admin@example.com",
      "username": "admin",
      "phone": "13800138000",
      "avatar": "https://example.com/avatar.jpg",
      "department": "技术部",
      "job_title": "高级工程师",
      "is_verified": true,
      "created_at": "2024-01-01T00:00:00Z",
      "last_login": "2024-01-01T12:00:00Z"
    }
  }
}
```

### 更新用户资料

**PUT/PATCH** `/api/users/update_profile/`

```bash
curl -X PATCH http://127.0.0.1:8000/api/users/update_profile/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "nickname": "我的昵称",
    "bio": "个人简介",
    "location": "北京市"
  }'
```

### 用户登出

**POST** `/api/users/logout/`

```bash
curl -X POST http://127.0.0.1:8000/api/users/logout/ \
  -H "Authorization: Token your-token-here"
```

## 🔑 Token 管理 API

### 获取 Token

**GET** `/api/users/get_token/`

```bash
curl -H "Authorization: Token your-token-here" \
     http://127.0.0.1:8000/api/users/get_token/
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "Token获取成功",
  "data": {
    "token": "your-token-here",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### 刷新 Token

**POST** `/api/users/refresh_token/`

```bash
curl -X POST http://127.0.0.1:8000/api/users/refresh_token/ \
  -H "Authorization: Token your-old-token"
```

### 撤销 Token

**DELETE** `/api/users/revoke_token/`

```bash
curl -X DELETE http://127.0.0.1:8000/api/users/revoke_token/ \
  -H "Authorization: Token your-token-here"
```

## 🌐 第三方登录 API

### 获取第三方登录提供商

**GET** `/api/users/third_party_providers/`

```bash
curl http://127.0.0.1:8000/api/users/third_party_providers/
```

**响应示例**:
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
        "corp_id": "your-corp-id",
        "client_id": "your-client-id"
      },
      {
        "name": "wechat_work",
        "display_name": "企业微信",
        "corp_id": "your-corp-id",
        "agent_id": "your-agent-id"
      }
    ]
  }
}
```

### 第三方登录跳转

**GET** `/api/users/third_party_auth/?provider=dingtalk`

```bash
# 浏览器访问，会自动跳转到第三方登录页面
curl -L http://127.0.0.1:8000/api/users/third_party_auth/?provider=dingtalk
```

### 第三方登录回调

**GET** `/api/users/third_party_callback/?state=dingtalk_login&code=auth_code`

> 此接口由第三方平台回调，通常不需要手动调用

### 同步第三方用户

**POST** `/api/users/sync_users/`

```bash
curl -X POST http://127.0.0.1:8000/api/users/sync_users/ \
  -H "Authorization: Token admin-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "dingtalk"
  }'
```

**权限要求**: 需要 `user_management` 模块的 `change` 权限

## 🔐 权限管理 API

### 获取用户模块权限

**GET** `/api/users/my_modules/`

```bash
curl -H "Authorization: Token your-token-here" \
     http://127.0.0.1:8000/api/users/my_modules/
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "获取用户模块权限成功",
  "data": {
    "modules": [
      {
        "name": "user_management",
        "display_name": "用户管理",
        "description": "用户和权限管理模块",
        "icon": "user",
        "url_pattern": "/admin/users/",
        "permissions": {
          "can_view": true,
          "can_add": true,
          "can_change": true,
          "can_delete": false
        }
      }
    ],
    "user_info": {
      "username": "admin",
      "email": "admin@example.com",
      "department": "技术部",
      "job_title": "系统管理员",
      "is_superuser": true
    }
  }
}
```

### 检查登录状态

**GET** `/api/users/check_login_status/`

```bash
curl http://127.0.0.1:8000/api/users/check_login_status/
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "状态检查成功",
  "data": {
    "logged_in": false
  }
}
```

## 📝 API 使用示例

### JavaScript/Fetch 示例

```javascript
// 用户登录
async function login(email, password) {
  try {
    const response = await fetch('/api/users/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    
    if (data.success) {
      // 保存 Token
      localStorage.setItem('token', data.data.token);
      console.log('登录成功:', data.data.user);
    } else {
      console.error('登录失败:', data.message);
    }
  } catch (error) {
    console.error('请求失败:', error);
  }
}

// 获取用户信息
async function getUserProfile() {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch('/api/users/profile/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('用户信息:', data.data.user);
    } else {
      console.error('获取失败:', data.message);
    }
  } catch (error) {
    console.error('请求失败:', error);
  }
}
```

### Python/Requests 示例

```python
import requests

class RookieAPI:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.session = requests.Session()
    
    def login(self, email, password):
        """用户登录"""
        url = f"{self.base_url}/api/users/login/"
        data = {"email": email, "password": password}
        
        response = self.session.post(url, json=data)
        result = response.json()
        
        if result.get('success'):
            self.token = result['data']['token']
            self.session.headers.update({
                'Authorization': f'Token {self.token}'
            })
            return result['data']['user']
        else:
            raise Exception(result.get('message', '登录失败'))
    
    def get_profile(self):
        """获取用户信息"""
        url = f"{self.base_url}/api/users/profile/"
        response = self.session.get(url)
        result = response.json()
        
        if result.get('success'):
            return result['data']['user']
        else:
            raise Exception(result.get('message', '获取用户信息失败'))
    
    def get_modules(self):
        """获取用户模块权限"""
        url = f"{self.base_url}/api/users/my_modules/"
        response = self.session.get(url)
        result = response.json()
        
        if result.get('success'):
            return result['data']['modules']
        else:
            raise Exception(result.get('message', '获取模块权限失败'))

# 使用示例
api = RookieAPI('http://127.0.0.1:8000')

try:
    # 登录
    user = api.login('admin@example.com', 'password123')
    print(f"登录成功: {user['email']}")
    
    # 获取用户信息
    profile = api.get_profile()
    print(f"用户部门: {profile['department']}")
    
    # 获取模块权限
    modules = api.get_modules()
    for module in modules:
        print(f"模块: {module['display_name']}")
        
except Exception as e:
    print(f"API调用失败: {e}")
```

### cURL 脚本示例

```bash
#!/bin/bash

# 配置
BASE_URL="http://127.0.0.1:8000"
EMAIL="admin@example.com"
PASSWORD="password123"

# 登录获取Token
echo "正在登录..."
LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/users/login/" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")

# 提取Token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.data.token')

if [ "$TOKEN" = "null" ]; then
    echo "登录失败"
    echo $LOGIN_RESPONSE | jq '.'
    exit 1
fi

echo "登录成功，Token: ${TOKEN:0:20}..."

# 获取用户信息
echo "获取用户信息..."
curl -s -H "Authorization: Token $TOKEN" \
     "${BASE_URL}/api/users/profile/" | jq '.'

# 获取模块权限
echo "获取模块权限..."
curl -s -H "Authorization: Token $TOKEN" \
     "${BASE_URL}/api/users/my_modules/" | jq '.data.modules'
```

## 🚨 错误处理

### 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 1001 | Token无效或过期 | 重新登录获取新Token |
| 1002 | 权限不足 | 联系管理员分配权限 |
| 1003 | 用户不存在 | 检查用户名或邮箱 |
| 1004 | 密码错误 | 检查密码或重置密码 |
| 1005 | 账户被禁用 | 联系管理员激活账户 |
| 2001 | 参数验证失败 | 检查请求参数格式 |
| 2002 | 必填参数缺失 | 补充必填参数 |
| 3001 | 第三方登录配置错误 | 检查第三方应用配置 |
| 3002 | 第三方服务不可用 | 稍后重试或联系管理员 |

### 错误处理最佳实践

```javascript
async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });
    
    const data = await response.json();
    
    if (!data.success) {
      // 处理业务错误
      switch (data.code) {
        case 1001:
          // Token过期，重新登录
          redirectToLogin();
          break;
        case 1002:
          // 权限不足
          showPermissionError();
          break;
        default:
          showError(data.message);
      }
      throw new Error(data.message);
    }
    
    return data.data;
    
  } catch (error) {
    console.error('API请求失败:', error);
    throw error;
  }
}
```

## 📊 API 文档

### Swagger UI

访问 `http://your-domain.com/api/docs/` 查看交互式API文档

### ReDoc

访问 `http://your-domain.com/api/redoc/` 查看美观的API文档

### OpenAPI Schema

访问 `http://your-domain.com/api/schema/` 获取OpenAPI规范文件

## 🔧 开发工具

### Postman 集合

```json
{
  "info": {
    "name": "Rookie API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000"
    },
    {
      "key": "token",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "用户登录",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"admin@example.com\",\n  \"password\": \"password123\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/users/login/",
          "host": ["{{base_url}}"],
          "path": ["api", "users", "login", ""]
        }
      }
    }
  ]
}
```

### API 测试脚本

```python
# test_api.py
import unittest
import requests

class TestRookieAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.email = 'admin@example.com'
        self.password = 'password123'
        self.token = None
    
    def test_login(self):
        """测试用户登录"""
        url = f"{self.base_url}/api/users/login/"
        data = {"email": self.email, "password": self.password}
        
        response = requests.post(url, json=data)
        result = response.json()
        
        self.assertTrue(result['success'])
        self.assertIn('token', result['data'])
        self.token = result['data']['token']
    
    def test_get_profile(self):
        """测试获取用户信息"""
        if not self.token:
            self.test_login()
        
        url = f"{self.base_url}/api/users/profile/"
        headers = {'Authorization': f'Token {self.token}'}
        
        response = requests.get(url, headers=headers)
        result = response.json()
        
        self.assertTrue(result['success'])
        self.assertEqual(result['data']['user']['email'], self.email)

if __name__ == '__main__':
    unittest.main()
```

---

## 📞 技术支持

如果在使用API过程中遇到问题，可以通过以下方式获取帮助：

- 📧 **技术支持**: api-support@rookie.com
- 💬 **开发者社区**: [GitHub Discussions](https://github.com/degary/RooKie/discussions)
- 🐛 **Bug报告**: [GitHub Issues](https://github.com/degary/RooKie/issues)
- 📖 **详细文档**: [完整文档](docs/README.md)

---

**最后更新**: 2024-01-01  
**API版本**: v1.0.0