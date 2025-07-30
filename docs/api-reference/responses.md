# 响应格式

## 📋 概述

本文档详细说明 Rookie 项目 API 的统一响应格式、错误码定义和处理规范。

## 🎯 统一响应格式

### 标准响应结构
```json
{
  "success": true,                    // 布尔值，请求是否成功
  "code": 200,                       // 整数，HTTP状态码
  "message": "操作成功",              // 字符串，响应消息
  "data": {...},                     // 对象，响应数据（可选）
  "timestamp": "2024-01-01T12:00:00Z", // 字符串，ISO格式时间戳
  "request_id": "abc12345"           // 字符串，请求唯一标识
}
```

### 字段说明

#### success
- **类型**: Boolean
- **说明**: 表示请求是否成功处理
- **取值**: `true` 表示成功，`false` 表示失败

#### code
- **类型**: Integer
- **说明**: HTTP状态码，与响应头中的状态码一致
- **范围**: 100-599

#### message
- **类型**: String
- **说明**: 人类可读的响应消息
- **语言**: 中文（可根据Accept-Language调整）

#### data
- **类型**: Object | Array | null
- **说明**: 具体的响应数据
- **可选**: 某些接口可能不返回data字段

#### timestamp
- **类型**: String
- **说明**: 服务器处理请求的时间戳
- **格式**: ISO 8601格式 (YYYY-MM-DDTHH:mm:ss.sssZ)

#### request_id
- **类型**: String
- **说明**: 请求的唯一标识符，用于日志追踪
- **格式**: 8位随机字符串

## ✅ 成功响应

### 基本成功响应
```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "abc12345"
}
```

### 带数据的成功响应
```json
{
  "success": true,
  "code": 200,
  "message": "获取用户信息成功",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "testuser"
    }
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "def67890"
}
```

### 创建成功响应
```json
{
  "success": true,
  "code": 201,
  "message": "用户创建成功",
  "data": {
    "user": {
      "id": 2,
      "email": "newuser@example.com",
      "username": "newuser"
    }
  },
  "timestamp": "2024-01-01T12:05:00Z",
  "request_id": "ghi12345"
}
```

### 列表数据响应
```json
{
  "success": true,
  "code": 200,
  "message": "获取用户列表成功",
  "data": {
    "users": [
      {
        "id": 1,
        "email": "user1@example.com",
        "username": "user1"
      },
      {
        "id": 2,
        "email": "user2@example.com",
        "username": "user2"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_count": 100,
      "page_size": 20,
      "has_next": true,
      "has_previous": false
    }
  },
  "timestamp": "2024-01-01T12:10:00Z",
  "request_id": "jkl67890"
}
```

## ❌ 错误响应

### 基本错误响应
```json
{
  "success": false,
  "code": 400,
  "message": "请求参数错误",
  "timestamp": "2024-01-01T12:15:00Z",
  "request_id": "mno12345"
}
```

### 带详细错误信息的响应
```json
{
  "success": false,
  "code": 422,
  "message": "数据验证失败",
  "data": {
    "email": ["邮箱格式不正确"],
    "password": ["密码长度至少8位"],
    "username": ["用户名已存在"]
  },
  "timestamp": "2024-01-01T12:20:00Z",
  "request_id": "pqr67890"
}
```

### 权限错误响应
```json
{
  "success": false,
  "code": 403,
  "message": "权限不足，需要用户管理权限",
  "data": {
    "required_permission": "user_management.view",
    "user_permissions": ["notification.view", "file_management.view"]
  },
  "timestamp": "2024-01-01T12:25:00Z",
  "request_id": "stu12345"
}
```

## 🚨 错误码定义

### HTTP标准错误码

#### 2xx 成功
| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 请求成功但无返回内容 |

#### 4xx 客户端错误
| 状态码 | 说明 | 使用场景 | 解决方案 |
|--------|------|----------|----------|
| 400 | Bad Request | 请求参数错误 | 检查请求参数格式 |
| 401 | Unauthorized | 未授权访问 | 检查Token或重新登录 |
| 403 | Forbidden | 权限不足 | 联系管理员分配权限 |
| 404 | Not Found | 资源不存在 | 检查请求路径和资源ID |
| 405 | Method Not Allowed | 请求方法不允许 | 检查HTTP方法 |
| 422 | Unprocessable Entity | 数据验证失败 | 检查数据格式和必填字段 |
| 429 | Too Many Requests | 请求频率过高 | 降低请求频率 |

#### 5xx 服务器错误
| 状态码 | 说明 | 使用场景 | 解决方案 |
|--------|------|----------|----------|
| 500 | Internal Server Error | 服务器内部错误 | 联系技术支持 |
| 502 | Bad Gateway | 网关错误 | 检查服务器状态 |
| 503 | Service Unavailable | 服务不可用 | 稍后重试 |
| 504 | Gateway Timeout | 网关超时 | 检查网络连接 |

### 业务错误码

#### 1xxx 用户相关错误
| 错误码 | 说明 | 示例场景 |
|--------|------|----------|
| 1001 | 用户不存在 | 查询不存在的用户ID |
| 1002 | 用户已存在 | 注册时邮箱已被使用 |
| 1003 | 密码错误 | 登录时密码不正确 |
| 1004 | 账户被禁用 | 用户账户被管理员禁用 |
| 1005 | 邮箱未验证 | 需要验证邮箱才能操作 |

#### 2xxx 权限相关错误
| 错误码 | 说明 | 示例场景 |
|--------|------|----------|
| 2001 | 权限不足 | 访问需要特定权限的接口 |
| 2002 | 角色不存在 | 分配不存在的用户角色 |
| 2003 | 权限配置错误 | 权限配置格式不正确 |

#### 3xxx 第三方集成错误
| 错误码 | 说明 | 示例场景 |
|--------|------|----------|
| 3001 | 第三方认证失败 | 钉钉登录授权失败 |
| 3002 | 第三方配置错误 | 第三方应用配置不正确 |
| 3003 | 第三方服务不可用 | 第三方服务临时不可用 |

## 📊 响应示例集合

### 用户注册成功
```json
{
  "success": true,
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 3,
      "email": "newuser@example.com",
      "username": "newuser",
      "is_active": true,
      "date_joined": "2024-01-01T12:30:00Z"
    }
  },
  "timestamp": "2024-01-01T12:30:00Z",
  "request_id": "vwx12345"
}
```

### 登录失败
```json
{
  "success": false,
  "code": 422,
  "message": "登录信息验证失败",
  "data": {
    "non_field_errors": ["邮箱或密码错误"]
  },
  "timestamp": "2024-01-01T12:35:00Z",
  "request_id": "yzab6789"
}
```

### Token无效
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问",
  "data": {
    "error_type": "invalid_token",
    "error_description": "Token已过期或无效"
  },
  "timestamp": "2024-01-01T12:40:00Z",
  "request_id": "cdef1234"
}
```

### 权限不足
```json
{
  "success": false,
  "code": 403,
  "message": "权限不足",
  "data": {
    "required_permission": "user_management.delete",
    "error_type": "permission_denied",
    "error_description": "需要用户管理删除权限"
  },
  "timestamp": "2024-01-01T12:45:00Z",
  "request_id": "ghij5678"
}
```

### 资源不存在
```json
{
  "success": false,
  "code": 404,
  "message": "用户不存在",
  "data": {
    "resource_type": "user",
    "resource_id": 999,
    "error_type": "resource_not_found"
  },
  "timestamp": "2024-01-01T12:50:00Z",
  "request_id": "klmn9012"
}
```

### 服务器错误
```json
{
  "success": false,
  "code": 500,
  "message": "服务器内部错误",
  "data": {
    "error_type": "internal_error",
    "error_id": "ERR_20240101_001",
    "support_contact": "support@rookie.com"
  },
  "timestamp": "2024-01-01T12:55:00Z",
  "request_id": "opqr3456"
}
```

## 🔧 客户端处理建议

### JavaScript处理示例
```javascript
async function handleAPIResponse(response) {
  const data = await response.json();

  if (data.success) {
    // 成功处理
    console.log('操作成功:', data.message);
    return data.data;
  } else {
    // 错误处理
    switch (data.code) {
      case 401:
        // Token无效，重新登录
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
        break;
      case 403:
        // 权限不足
        showError('权限不足: ' + data.message);
        break;
      case 422:
        // 数据验证失败
        showValidationErrors(data.data);
        break;
      case 500:
        // 服务器错误
        showError('服务器错误，请稍后重试');
        break;
      default:
        showError(data.message);
    }
    throw new Error(data.message);
  }
}

// 使用示例
try {
  const response = await fetch('/api/users/profile/', {
    headers: { 'Authorization': `Token ${token}` }
  });
  const userData = await handleAPIResponse(response);
  console.log('用户数据:', userData);
} catch (error) {
  console.error('请求失败:', error.message);
}
```

### Python处理示例
```python
import requests
from typing import Dict, Any

class APIException(Exception):
    def __init__(self, message: str, code: int, data: Dict = None):
        self.message = message
        self.code = code
        self.data = data or {}
        super().__init__(message)

def handle_api_response(response: requests.Response) -> Dict[str, Any]:
    """处理API响应"""
    try:
        data = response.json()
    except ValueError:
        raise APIException("响应格式错误", response.status_code)

    if data.get('success'):
        return data.get('data', {})
    else:
        code = data.get('code', response.status_code)
        message = data.get('message', '请求失败')
        error_data = data.get('data', {})

        # 根据错误码进行特殊处理
        if code == 401:
            # Token无效，清除本地存储
            print("Token无效，需要重新登录")
        elif code == 403:
            print(f"权限不足: {message}")
        elif code == 422:
            print(f"数据验证失败: {error_data}")
        elif code >= 500:
            print(f"服务器错误: {message}")

        raise APIException(message, code, error_data)

# 使用示例
try:
    response = requests.get('/api/users/profile/',
                          headers={'Authorization': f'Token {token}'})
    user_data = handle_api_response(response)
    print('用户数据:', user_data)
except APIException as e:
    print(f'API错误 [{e.code}]: {e.message}')
    if e.data:
        print('错误详情:', e.data)
```

## 📝 最佳实践

### 客户端开发建议
1. **统一错误处理**: 建立统一的错误处理机制
2. **重试机制**: 对于5xx错误实现重试逻辑
3. **用户友好**: 将技术错误转换为用户友好的提示
4. **日志记录**: 记录request_id用于问题追踪

### 服务端开发建议
1. **一致性**: 确保所有接口都遵循统一格式
2. **详细信息**: 在data字段中提供足够的错误详情
3. **国际化**: 支持多语言错误消息
4. **监控**: 基于错误码建立监控和告警

## 🔗 相关文档

- [认证接口](authentication.md) - 认证相关接口
- [用户接口](users.md) - 用户管理接口
- [故障排除](../troubleshooting/error-codes.md) - 错误码详细说明
