# 用户接口

## 📋 概述

用户接口提供用户信息管理、资料更新、权限查询等功能。

## 👥 用户信息管理

### 获取用户信息

**接口地址**: `GET /api/users/profile/`  
**认证要求**: Token或Session  
**权限要求**: 已登录用户

#### 响应示例
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
      "phone": "13800138000",
      "avatar": "https://example.com/avatar.jpg",
      "department": "技术部",
      "job_title": "高级工程师",
      "employee_id": "E001",
      "auth_source": "local",
      "external_id": null,
      "is_active": true,
      "is_superuser": true,
      "is_verified": true,
      "date_joined": "2024-01-01T10:00:00Z",
      "last_login": "2024-01-01T12:00:00Z"
    }
  }
}
```

### 更新用户资料

**接口地址**: `PATCH /api/users/update_profile/`  
**认证要求**: Token或Session  
**权限要求**: 已登录用户

#### 请求参数
```json
{
  "phone": "13800138000",        // 可选，手机号
  "department": "技术部",         // 可选，部门
  "job_title": "高级工程师",      // 可选，职位
  "bio": "个人简介",             // 可选，个人简介
  "avatar": "头像URL",           // 可选，头像地址
  "preferences": {               // 可选，个人偏好
    "theme": "dark",
    "language": "zh-CN"
  }
}
```

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "用户资料更新成功",
  "data": {
    "profile": {
      "id": 1,
      "user": 1,
      "bio": "个人简介",
      "avatar": "头像URL",
      "preferences": {
        "theme": "dark",
        "language": "zh-CN"
      },
      "updated_at": "2024-01-01T12:30:00Z"
    }
  }
}
```

## 🔑 权限查询

### 获取用户权限模块

**接口地址**: `GET /api/users/my_modules/`  
**认证要求**: Token或Session  
**权限要求**: 已登录用户

#### 响应示例
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
          "can_delete": false
        }
      },
      {
        "name": "system_config",
        "display_name": "系统配置",
        "description": "系统参数和配置管理",
        "icon": "fas fa-cogs",
        "url_pattern": "/admin/config/",
        "permissions": {
          "can_view": true,
          "can_add": false,
          "can_change": true,
          "can_delete": false
        }
      }
    ],
    "user_info": {
      "username": "admin",
      "email": "admin@example.com",
      "department": "技术部",
      "job_title": "高级工程师",
      "is_superuser": true
    }
  }
}
```

## 📊 用户统计

### 获取用户统计信息

**接口地址**: `GET /api/users/statistics/`  
**认证要求**: Token或Session  
**权限要求**: 数据分析查看权限

#### 响应示例
```json
{
  "success": true,
  "code": 200,
  "message": "获取统计信息成功",
  "data": {
    "total_users": 150,
    "active_users": 142,
    "new_users_today": 5,
    "new_users_this_week": 23,
    "new_users_this_month": 87,
    "login_methods": {
      "local": 80,
      "dingtalk": 45,
      "wechat_work": 25
    },
    "department_distribution": {
      "技术部": 60,
      "产品部": 30,
      "运营部": 25,
      "其他": 35
    }
  }
}
```

## 🔧 使用示例

### JavaScript示例
```javascript
class UserAPI {
  constructor(token) {
    this.token = token;
    this.baseURL = '/api/users';
  }
  
  async getProfile() {
    const response = await fetch(`${this.baseURL}/profile/`, {
      headers: {
        'Authorization': `Token ${this.token}`
      }
    });
    return response.json();
  }
  
  async updateProfile(data) {
    const response = await fetch(`${this.baseURL}/update_profile/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.token}`
      },
      body: JSON.stringify(data)
    });
    return response.json();
  }
  
  async getModules() {
    const response = await fetch(`${this.baseURL}/my_modules/`, {
      headers: {
        'Authorization': `Token ${this.token}`
      }
    });
    return response.json();
  }
}

// 使用示例
const userAPI = new UserAPI('your_token_here');

// 获取用户信息
const profile = await userAPI.getProfile();
console.log('用户信息:', profile.data.user);

// 更新用户资料
const updateResult = await userAPI.updateProfile({
  phone: '13800138000',
  department: '技术部'
});
console.log('更新结果:', updateResult.message);

// 获取权限模块
const modules = await userAPI.getModules();
console.log('可访问模块:', modules.data.modules);
```

### Python示例
```python
import requests

class UserAPI:
    def __init__(self, token, base_url="http://127.0.0.1:8000/api/users"):
        self.token = token
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
    
    def get_profile(self):
        """获取用户信息"""
        response = requests.get(f"{self.base_url}/profile/", headers=self.headers)
        return response.json()
    
    def update_profile(self, **kwargs):
        """更新用户资料"""
        response = requests.patch(
            f"{self.base_url}/update_profile/",
            json=kwargs,
            headers=self.headers
        )
        return response.json()
    
    def get_modules(self):
        """获取权限模块"""
        response = requests.get(f"{self.base_url}/my_modules/", headers=self.headers)
        return response.json()
    
    def get_statistics(self):
        """获取用户统计"""
        response = requests.get(f"{self.base_url}/statistics/", headers=self.headers)
        return response.json()

# 使用示例
user_api = UserAPI('your_token_here')

# 获取用户信息
profile = user_api.get_profile()
if profile['success']:
    user = profile['data']['user']
    print(f"用户: {user['username']} ({user['email']})")

# 更新用户资料
result = user_api.update_profile(
    phone='13800138000',
    department='技术部',
    job_title='高级工程师'
)
print(f"更新结果: {result['message']}")

# 获取权限模块
modules = user_api.get_modules()
if modules['success']:
    for module in modules['data']['modules']:
        print(f"模块: {module['display_name']} - 权限: {module['permissions']}")
```

## 🚨 错误处理

### 常见错误

#### 用户信息不存在
```json
{
  "success": false,
  "code": 404,
  "message": "用户不存在"
}
```

#### 权限不足
```json
{
  "success": false,
  "code": 403,
  "message": "权限不足，无法访问用户统计信息"
}
```

#### 数据验证失败
```json
{
  "success": false,
  "code": 422,
  "message": "数据验证失败",
  "data": {
    "phone": ["手机号格式不正确"],
    "email": ["邮箱已被使用"]
  }
}
```

## 🔗 相关文档

- [认证接口](authentication.md) - 用户登录和Token管理
- [权限接口](permissions.md) - 权限管理相关接口
- [响应格式](responses.md) - 统一响应格式说明