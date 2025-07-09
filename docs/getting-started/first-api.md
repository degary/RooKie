# 第一个API

## 📋 概述

本文档通过实际示例，指导您完成第一个API调用，了解Rookie项目的API使用方法。

## 🎯 学习目标

- 了解API认证机制
- 掌握Token的获取和使用
- 学会调用基本的API接口
- 理解统一的响应格式

## 🚀 API调用实践

### 前置条件
- 项目已启动 (参考 [快速开始](quick-start.md))
- 已创建超级用户或使用演示数据

### 1. 获取API Token

#### 方法1: 通过登录API获取
```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

**响应示例:**
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1,
      "email": "admin@example.com",
      "username": "admin",
      "department": null,
      "job_title": null,
      "is_superuser": true
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "abc12345"
}
```

#### 保存Token
```bash
# 从响应中复制token值
export TOKEN="9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### 2. 使用Token调用API

#### 获取用户信息
```bash
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/
```

**响应示例:**
```json
{
  "success": true,
  "code": 200,
  "message": "获取用户信息成功",
  "data": {
    "user": {
      "id": 1,
      "email": "admin@example.com",
      "username": "admin",
      "phone": null,
      "avatar": null,
      "department": null,
      "job_title": null,
      "employee_id": null,
      "is_active": true,
      "is_superuser": true,
      "date_joined": "2024-01-01T10:00:00Z"
    }
  },
  "timestamp": "2024-01-01T12:01:00Z",
  "request_id": "def67890"
}
```

#### 获取用户权限模块
```bash
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/my_modules/
```

**响应示例:**
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
        "description": "用户和权限管理功能",
        "icon": "fas fa-users",
        "url_pattern": "/admin/users/",
        "permissions": {
          "can_view": true,
          "can_add": true,
          "can_change": true,
          "can_delete": true
        }
      }
    ],
    "user_info": {
      "username": "admin",
      "email": "admin@example.com",
      "department": null,
      "job_title": null,
      "is_superuser": true
    }
  }
}
```

### 3. Token管理

#### 获取当前Token信息
```bash
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/get_token/
```

#### 刷新Token
```bash
curl -X POST http://127.0.0.1:8000/api/users/refresh_token/ \
  -H "Authorization: Token $TOKEN"
```

**响应示例:**
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

#### 撤销Token
```bash
curl -X DELETE http://127.0.0.1:8000/api/users/revoke_token/ \
  -H "Authorization: Token $TOKEN"
```

## 🐍 Python客户端示例

### 基础示例
```python
import requests
import json

class RookieAPIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
    
    def login(self, email, password):
        """用户登录获取Token"""
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
            raise Exception(f"登录失败: {result.get('message')}")
    
    def get_profile(self):
        """获取用户信息"""
        url = f"{self.base_url}/api/users/profile/"
        response = self.session.get(url)
        result = response.json()
        
        if result.get('success'):
            return result['data']['user']
        else:
            raise Exception(f"获取用户信息失败: {result.get('message')}")
    
    def get_modules(self):
        """获取用户权限模块"""
        url = f"{self.base_url}/api/users/my_modules/"
        response = self.session.get(url)
        result = response.json()
        
        if result.get('success'):
            return result['data']
        else:
            raise Exception(f"获取权限模块失败: {result.get('message')}")

# 使用示例
if __name__ == "__main__":
    client = RookieAPIClient()
    
    try:
        # 登录
        user = client.login("admin@example.com", "password123")
        print(f"登录成功: {user['email']}")
        
        # 获取用户信息
        profile = client.get_profile()
        print(f"用户信息: {profile['username']}")
        
        # 获取权限模块
        modules_data = client.get_modules()
        print(f"可访问模块数量: {len(modules_data['modules'])}")
        
        for module in modules_data['modules']:
            print(f"- {module['display_name']}: {module['permissions']}")
            
    except Exception as e:
        print(f"错误: {e}")
```

### 异步示例
```python
import aiohttp
import asyncio

class AsyncRookieAPIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
    
    async def login(self, email, password):
        """异步登录"""
        url = f"{self.base_url}/api/users/login/"
        data = {"email": email, "password": password}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                result = await response.json()
                
                if result.get('success'):
                    self.token = result['data']['token']
                    return result['data']['user']
                else:
                    raise Exception(f"登录失败: {result.get('message')}")
    
    async def get_profile(self):
        """异步获取用户信息"""
        url = f"{self.base_url}/api/users/profile/"
        headers = {'Authorization': f'Token {self.token}'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                result = await response.json()
                
                if result.get('success'):
                    return result['data']['user']
                else:
                    raise Exception(f"获取用户信息失败: {result.get('message')}")

# 使用示例
async def main():
    client = AsyncRookieAPIClient()
    
    try:
        user = await client.login("admin@example.com", "password123")
        print(f"异步登录成功: {user['email']}")
        
        profile = await client.get_profile()
        print(f"异步获取用户信息: {profile['username']}")
        
    except Exception as e:
        print(f"错误: {e}")

# 运行异步示例
# asyncio.run(main())
```

## 📋 响应格式说明

### 统一响应结构
```json
{
  "success": true,          // 请求是否成功
  "code": 200,             // HTTP状态码
  "message": "操作成功",    // 响应消息
  "data": {...},           // 响应数据
  "timestamp": "2024-01-01T12:00:00Z",  // 时间戳
  "request_id": "abc12345" // 请求ID
}
```

### 成功响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "获取成功",
  "data": {
    "user": {...}
  }
}
```

### 错误响应示例
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问",
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "def67890"
}
```

## 🔧 调试技巧

### 1. 查看详细响应
```bash
# 使用 -v 参数查看详细信息
curl -v -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/
```

### 2. 格式化JSON响应
```bash
# 使用 jq 格式化JSON
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/ | jq
```

### 3. 保存响应到文件
```bash
# 保存响应用于分析
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/ > response.json
```

## ❗ 常见错误

### 401 未授权
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问"
}
```
**解决方案**: 检查Token是否正确，是否已过期

### 403 权限不足
```json
{
  "success": false,
  "code": 403,
  "message": "权限不足"
}
```
**解决方案**: 检查用户是否有相应的权限

### 404 接口不存在
```json
{
  "success": false,
  "code": 404,
  "message": "资源不存在"
}
```
**解决方案**: 检查API路径是否正确

## 🔗 下一步

完成第一个API调用后，建议继续学习：

- [认证系统](../user-guide/authentication.md) - 深入了解认证机制
- [API参考](../api-reference/README.md) - 完整的API接口文档
- [Token认证教程](../tutorials/token-auth-tutorial.md) - 详细的Token使用教程