# Token认证测试指南

## 🧪 **完整测试方案**

### **测试环境准备**
```bash
# 启动服务器
python manage.py runserver
```

### **步骤1: 创建用户**

#### **方法A: 通过API注册**
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

**预期响应:**
```json
{
  "success": true,
  "code": 201,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 2,
      "email": "test@example.com",
      "username": "testuser"
    }
  }
}
```

#### **方法B: 使用现有用户**
```bash
# 如果已有admin用户，可直接使用
# 默认: admin@example.com / password123
```

### **步骤2: 登录获取Token**

```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
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
      "id": 2,
      "email": "test@example.com",
      "username": "testuser"
    },
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
  }
}
```

**保存Token:**
```bash
# 复制响应中的token值
export TOKEN="4980b51cd1dd16106e00e0fb728bb09f0b1dfe2a"
```

### **步骤3: 使用Token访问API**

#### **3.1 获取用户信息**
```bash
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/
```

**预期响应:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 2,
      "email": "test@example.com",
      "username": "testuser",
      "department": null,
      "job_title": null
    }
  },
  "message": "获取用户信息成功"
}
```

#### **3.2 获取用户模块权限**
```bash
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/my_modules/
```

#### **3.3 更新用户资料**
```bash
curl -X PATCH http://127.0.0.1:8000/api/users/update_profile/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "这是我的个人简介"
  }'
```

### **步骤4: Token管理测试**

#### **4.1 获取当前Token信息**
```bash
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/get_token/
```

**预期响应:**
```json
{
  "success": true,
  "data": {
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "created_at": "2024-01-01T12:00:00Z"
  },
  "message": "Token获取成功"
}
```

#### **4.2 刷新Token**
```bash
curl -X POST http://127.0.0.1:8000/api/users/refresh_token/ \
  -H "Authorization: Token $TOKEN"
```

**预期响应:**
```json
{
  "success": true,
  "data": {
    "token": "新的token字符串"
  },
  "message": "Token刷新成功"
}
```

**更新Token:**
```bash
export TOKEN="新的token字符串"
```

#### **4.3 撤销Token**
```bash
curl -X DELETE http://127.0.0.1:8000/api/users/revoke_token/ \
  -H "Authorization: Token $TOKEN"
```

**预期响应:**
```json
{
  "success": true,
  "data": {
    "deleted_count": 1
  },
  "message": "Token已撤销"
}
```

### **步骤5: 验证Token失效**

```bash
# 使用已撤销的Token访问API
curl -H "Authorization: Token $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/
```

**预期响应:**
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问"
}
```

### **步骤6: 错误场景测试**

#### **6.1 无效Token**
```bash
curl -H "Authorization: Token invalid_token" \
     http://127.0.0.1:8000/api/users/profile/
```

#### **6.2 缺少Token**
```bash
curl http://127.0.0.1:8000/api/users/profile/
```

#### **6.3 错误的Token格式**
```bash
curl -H "Authorization: Bearer $TOKEN" \
     http://127.0.0.1:8000/api/users/profile/
```

### **🐍 Python测试脚本**

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_token_auth():
    # 1. 注册用户
    register_data = {
        "email": "test@example.com",
        "username": "testuser", 
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/register/", json=register_data)
    print("注册响应:", response.json())
    
    # 2. 登录获取Token
    login_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/login/", json=login_data)
    result = response.json()
    token = result['data']['token']
    print("登录成功，Token:", token)
    
    # 3. 使用Token访问API
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(f"{BASE_URL}/api/users/profile/", headers=headers)
    print("用户信息:", response.json())
    
    # 4. 刷新Token
    response = requests.post(f"{BASE_URL}/api/users/refresh_token/", headers=headers)
    new_token = response.json()['data']['token']
    print("新Token:", new_token)
    
    # 5. 撤销Token
    headers = {"Authorization": f"Token {new_token}"}
    response = requests.delete(f"{BASE_URL}/api/users/revoke_token/", headers=headers)
    print("撤销结果:", response.json())

if __name__ == "__main__":
    test_token_auth()
```

### **✅ 测试检查清单**

- [ ] 用户注册成功
- [ ] 登录返回Token
- [ ] Token格式正确（40位字符串）
- [ ] 使用Token访问受保护API成功
- [ ] 获取Token信息成功
- [ ] 刷新Token成功
- [ ] 撤销Token成功
- [ ] 无效Token被拒绝
- [ ] 缺少Token被拒绝

### **🔧 常见问题**

#### **Q: Token格式错误**
A: 确保使用 `Authorization: Token your_token_here` 格式，不是 `Bearer`

#### **Q: 401未授权错误**
A: 检查Token是否正确，是否已过期或被撤销

#### **Q: CSRF错误**
A: Token认证不需要CSRF Token，确保使用正确的认证方式

#### **Q: 服务器500错误**
A: 检查服务器日志，可能是配置问题或数据库连接问题

完成以上测试即可验证Token认证功能正常工作！