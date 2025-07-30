# API使用指南

## 📋 概述

Rookie 项目提供完整的 RESTful API 接口，支持用户管理、权限控制、第三方登录等功能，适用于前端应用、移动端和第三方系统集成。

## 🌐 API基础

### 基础信息
- **Base URL**: `http://127.0.0.1:8000/api/`
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

### 统一响应格式
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

## 🔐 认证方式

### Token认证 (推荐)
```bash
# 请求头格式
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Session认证
```bash
# 通过Cookie自动携带
# 适用于同域名的Web应用
```

## 👥 用户相关API

### 用户注册
```bash
POST /api/users/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "newuser",
  "password": "password123",
  "password_confirm": "password123"
}
```

**响应示例:**
```json
{
  "success": true,
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 2,
      "email": "user@example.com",
      "username": "newuser"
    }
  }
}
```

### 用户登录
```bash
POST /api/users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应示例:**
```json
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 2,
      "email": "user@example.com",
      "username": "newuser"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  }
}
```

### 获取用户信息
```bash
GET /api/users/profile/
Authorization: Token your_token_here
```

### 更新用户资料
```bash
PATCH /api/users/update_profile/
Authorization: Token your_token_here
Content-Type: application/json

{
  "phone": "13800138000",
  "department": "技术部",
  "job_title": "高级工程师"
}
```

### 用户登出
```bash
POST /api/users/logout/
Authorization: Token your_token_here
```

## 🔑 Token管理API

### 获取Token信息
```bash
GET /api/users/get_token/
Authorization: Token your_token_here
```

### 刷新Token
```bash
POST /api/users/refresh_token/
Authorization: Token your_token_here
```

### 撤销Token
```bash
DELETE /api/users/revoke_token/
Authorization: Token your_token_here
```

## 🔐 权限相关API

### 获取用户权限模块
```bash
GET /api/users/my_modules/
Authorization: Token your_token_here
```

**响应示例:**
```json
{
  "success": true,
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
      }
    ],
    "user_info": {
      "username": "newuser",
      "email": "user@example.com",
      "is_superuser": false
    }
  }
}
```

## 🌐 第三方登录API

### 获取登录提供商
```bash
GET /api/users/third_party_providers/
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "providers": [
      {
        "name": "dingtalk",
        "display_name": "钉钉登录",
        "auth_url": "https://oapi.dingtalk.com/connect/oauth2/sns_authorize?..."
      }
    ]
  }
}
```

### 第三方登录跳转
```bash
GET /api/users/third_party_auth/?provider=dingtalk
# 自动跳转到第三方登录页面
```

### 同步第三方用户
```bash
POST /api/users/sync_users/
Authorization: Token your_token_here
Content-Type: application/json

{
  "provider": "dingtalk"
}
```

## 📱 客户端集成示例

### JavaScript/Axios
```javascript
class RookieAPI {
  constructor(baseURL = 'http://127.0.0.1:8000/api') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');

    // 配置axios实例
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 请求拦截器 - 添加Token
    this.client.interceptors.request.use(config => {
      if (this.token) {
        config.headers.Authorization = `Token ${this.token}`;
      }
      return config;
    });

    // 响应拦截器 - 处理错误
    this.client.interceptors.response.use(
      response => response.data,
      error => {
        if (error.response?.status === 401) {
          this.logout();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // 用户登录
  async login(email, password) {
    const response = await this.client.post('/users/login/', {
      email,
      password
    });

    if (response.success) {
      this.token = response.data.token;
      localStorage.setItem('auth_token', this.token);
      return response.data.user;
    }
    throw new Error(response.message);
  }

  // 获取用户信息
  async getProfile() {
    const response = await this.client.get('/users/profile/');
    return response.data.user;
  }

  // 获取用户权限
  async getModules() {
    const response = await this.client.get('/users/my_modules/');
    return response.data;
  }

  // 用户登出
  async logout() {
    try {
      await this.client.post('/users/logout/');
    } finally {
      this.token = null;
      localStorage.removeItem('auth_token');
    }
  }
}

// 使用示例
const api = new RookieAPI();

// 登录
try {
  const user = await api.login('user@example.com', 'password123');
  console.log('登录成功:', user);
} catch (error) {
  console.error('登录失败:', error.message);
}
```

### Python/Requests
```python
import requests
from typing import Optional, Dict, Any

class RookieAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """统一请求方法"""
        url = f"{self.base_url}{endpoint}"

        if self.token:
            self.session.headers['Authorization'] = f'Token {self.token}'

        response = self.session.request(method, url, **kwargs)
        result = response.json()

        if not result.get('success'):
            raise Exception(f"API错误: {result.get('message')}")

        return result

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """用户登录"""
        data = {"email": email, "password": password}
        result = self._request('POST', '/users/login/', json=data)

        self.token = result['data']['token']
        return result['data']['user']

    def get_profile(self) -> Dict[str, Any]:
        """获取用户信息"""
        result = self._request('GET', '/users/profile/')
        return result['data']['user']

    def get_modules(self) -> Dict[str, Any]:
        """获取用户权限模块"""
        result = self._request('GET', '/users/my_modules/')
        return result['data']

    def update_profile(self, **kwargs) -> Dict[str, Any]:
        """更新用户资料"""
        result = self._request('PATCH', '/users/update_profile/', json=kwargs)
        return result['data']['profile']

    def logout(self) -> None:
        """用户登出"""
        try:
            self._request('POST', '/users/logout/')
        finally:
            self.token = None
            if 'Authorization' in self.session.headers:
                del self.session.headers['Authorization']

# 使用示例
client = RookieAPIClient()

try:
    # 登录
    user = client.login('user@example.com', 'password123')
    print(f"登录成功: {user['email']}")

    # 获取用户信息
    profile = client.get_profile()
    print(f"用户信息: {profile}")

    # 获取权限模块
    modules = client.get_modules()
    print(f"可访问模块: {len(modules['modules'])}")

except Exception as e:
    print(f"错误: {e}")
```

### React Hook示例
```javascript
import { useState, useEffect, createContext, useContext } from 'react';
import axios from 'axios';

// 创建API上下文
const APIContext = createContext();

// API Provider组件
export const APIProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('auth_token'));
  const [loading, setLoading] = useState(false);

  const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  // 请求拦截器
  api.interceptors.request.use(config => {
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  });

  // 响应拦截器
  api.interceptors.response.use(
    response => response.data,
    error => {
      if (error.response?.status === 401) {
        logout();
      }
      return Promise.reject(error);
    }
  );

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await api.post('/users/login/', { email, password });
      const { user, token } = response.data;

      setUser(user);
      setToken(token);
      localStorage.setItem('auth_token', token);

      return user;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('auth_token');
  };

  const getProfile = async () => {
    const response = await api.get('/users/profile/');
    return response.data.user;
  };

  useEffect(() => {
    if (token && !user) {
      getProfile().then(setUser).catch(() => logout());
    }
  }, [token]);

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    getProfile,
    api
  };

  return (
    <APIContext.Provider value={value}>
      {children}
    </APIContext.Provider>
  );
};

// 使用Hook
export const useAPI = () => {
  const context = useContext(APIContext);
  if (!context) {
    throw new Error('useAPI must be used within APIProvider');
  }
  return context;
};

// 组件中使用
const LoginForm = () => {
  const { login, loading } = useAPI();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      // 登录成功后的处理
    } catch (error) {
      console.error('登录失败:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="邮箱"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="密码"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? '登录中...' : '登录'}
      </button>
    </form>
  );
};
```

## 🚨 错误处理

### 常见错误码
- **400**: 请求参数错误
- **401**: 未授权访问
- **403**: 权限不足
- **404**: 资源不存在
- **422**: 数据验证失败
- **500**: 服务器内部错误

### 错误响应格式
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问",
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "def67890"
}
```

## 📊 API限制

### 请求频率
- 默认无限制
- 可根据需要配置限流

### 数据大小
- 请求体最大: 10MB
- 响应数据分页: 20条/页

## 🔗 相关文档

- [认证系统](authentication.md) - 认证方式详解
- [API参考](../api-reference/README.md) - 完整接口文档
- [Token认证教程](../tutorials/token-auth-tutorial.md) - 实践教程
