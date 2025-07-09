# 错误码说明

## 📋 概述

本文档详细说明 Rookie 项目中所有错误码的含义、触发条件和解决方案。

## 🚨 HTTP标准错误码

### 2xx 成功状态码

#### 200 OK
- **含义**: 请求成功
- **使用场景**: 正常的GET、POST、PUT、PATCH请求
- **响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {...}
}
```

#### 201 Created
- **含义**: 资源创建成功
- **使用场景**: POST请求成功创建新资源
- **响应示例**:
```json
{
  "success": true,
  "code": 201,
  "message": "用户创建成功",
  "data": {
    "user": {...}
  }
}
```

#### 204 No Content
- **含义**: 请求成功但无返回内容
- **使用场景**: DELETE请求成功删除资源
- **响应示例**: 无响应体

### 4xx 客户端错误码

#### 400 Bad Request
- **含义**: 请求参数错误
- **常见原因**:
  - JSON格式错误
  - 必填参数缺失
  - 参数类型错误
- **解决方案**: 检查请求参数格式和内容
- **响应示例**:
```json
{
  "success": false,
  "code": 400,
  "message": "请求参数错误",
  "data": {
    "error": "JSON格式不正确"
  }
}
```

#### 401 Unauthorized
- **含义**: 未授权访问
- **常见原因**:
  - Token无效或过期
  - 未提供认证信息
  - Session过期
- **解决方案**: 
  - 检查Token格式: `Authorization: Token your_token_here`
  - 重新登录获取新Token
  - 检查Session状态
- **响应示例**:
```json
{
  "success": false,
  "code": 401,
  "message": "未授权访问",
  "data": {
    "error_type": "invalid_token",
    "error_description": "Token已过期或无效"
  }
}
```

#### 403 Forbidden
- **含义**: 权限不足
- **常见原因**:
  - 用户没有相应的模块权限
  - 用户账户被禁用
  - 访问被限制的资源
- **解决方案**:
  - 联系管理员分配权限
  - 检查用户组权限配置
  - 确认账户状态正常
- **响应示例**:
```json
{
  "success": false,
  "code": 403,
  "message": "权限不足",
  "data": {
    "required_permission": "user_management.view",
    "user_permissions": ["notification.view"]
  }
}
```

#### 404 Not Found
- **含义**: 资源不存在
- **常见原因**:
  - URL路径错误
  - 资源ID不存在
  - 接口不存在
- **解决方案**:
  - 检查URL路径
  - 确认资源ID正确
  - 查看API文档确认接口地址
- **响应示例**:
```json
{
  "success": false,
  "code": 404,
  "message": "用户不存在",
  "data": {
    "resource_type": "user",
    "resource_id": 999
  }
}
```

#### 405 Method Not Allowed
- **含义**: 请求方法不允许
- **常见原因**:
  - 使用了错误的HTTP方法
  - 接口不支持该方法
- **解决方案**: 检查API文档确认正确的HTTP方法
- **响应示例**:
```json
{
  "success": false,
  "code": 405,
  "message": "请求方法不允许",
  "data": {
    "allowed_methods": ["GET", "POST"]
  }
}
```

#### 422 Unprocessable Entity
- **含义**: 数据验证失败
- **常见原因**:
  - 数据格式不符合要求
  - 必填字段缺失
  - 数据类型错误
  - 业务规则验证失败
- **解决方案**: 根据错误详情修正数据
- **响应示例**:
```json
{
  "success": false,
  "code": 422,
  "message": "数据验证失败",
  "data": {
    "email": ["邮箱格式不正确"],
    "password": ["密码长度至少8位"],
    "username": ["用户名已存在"]
  }
}
```

#### 429 Too Many Requests
- **含义**: 请求频率过高
- **常见原因**: 超过API调用频率限制
- **解决方案**: 降低请求频率，稍后重试
- **响应示例**:
```json
{
  "success": false,
  "code": 429,
  "message": "请求频率过高",
  "data": {
    "retry_after": 60,
    "limit": "1000/hour"
  }
}
```

### 5xx 服务器错误码

#### 500 Internal Server Error
- **含义**: 服务器内部错误
- **常见原因**:
  - 代码异常
  - 数据库连接失败
  - 配置错误
- **解决方案**: 
  - 查看服务器日志
  - 联系技术支持
  - 检查服务器状态
- **响应示例**:
```json
{
  "success": false,
  "code": 500,
  "message": "服务器内部错误",
  "data": {
    "error_id": "ERR_20240101_001",
    "support_contact": "support@rookie.com"
  }
}
```

#### 502 Bad Gateway
- **含义**: 网关错误
- **常见原因**: 上游服务器响应无效
- **解决方案**: 检查服务器配置和网络连接

#### 503 Service Unavailable
- **含义**: 服务不可用
- **常见原因**: 服务器维护或过载
- **解决方案**: 稍后重试

#### 504 Gateway Timeout
- **含义**: 网关超时
- **常见原因**: 上游服务器响应超时
- **解决方案**: 检查网络连接和服务器性能

## 🔢 业务错误码

### 1xxx 用户相关错误

#### 1001 用户不存在
- **触发条件**: 查询不存在的用户ID
- **解决方案**: 确认用户ID正确
- **示例**:
```json
{
  "success": false,
  "code": 1001,
  "message": "用户不存在",
  "data": {
    "user_id": 999
  }
}
```

#### 1002 用户已存在
- **触发条件**: 注册时邮箱已被使用
- **解决方案**: 使用其他邮箱或找回密码
- **示例**:
```json
{
  "success": false,
  "code": 1002,
  "message": "用户已存在",
  "data": {
    "email": "user@example.com"
  }
}
```

#### 1003 密码错误
- **触发条件**: 登录时密码不正确
- **解决方案**: 确认密码正确或重置密码
- **示例**:
```json
{
  "success": false,
  "code": 1003,
  "message": "密码错误",
  "data": {
    "attempts_remaining": 3
  }
}
```

#### 1004 账户被禁用
- **触发条件**: 用户账户被管理员禁用
- **解决方案**: 联系管理员激活账户
- **示例**:
```json
{
  "success": false,
  "code": 1004,
  "message": "账户已被禁用",
  "data": {
    "disabled_at": "2024-01-01T12:00:00Z",
    "reason": "违反使用条款"
  }
}
```

#### 1005 邮箱未验证
- **触发条件**: 需要验证邮箱才能操作
- **解决方案**: 验证邮箱后重试
- **示例**:
```json
{
  "success": false,
  "code": 1005,
  "message": "邮箱未验证",
  "data": {
    "verification_sent": true
  }
}
```

### 2xxx 权限相关错误

#### 2001 权限不足
- **触发条件**: 访问需要特定权限的接口
- **解决方案**: 联系管理员分配权限
- **示例**:
```json
{
  "success": false,
  "code": 2001,
  "message": "权限不足",
  "data": {
    "required_permission": "user_management.delete",
    "current_permissions": ["user_management.view"]
  }
}
```

#### 2002 角色不存在
- **触发条件**: 分配不存在的用户角色
- **解决方案**: 确认角色名称正确
- **示例**:
```json
{
  "success": false,
  "code": 2002,
  "message": "角色不存在",
  "data": {
    "role_name": "invalid_role"
  }
}
```

#### 2003 权限配置错误
- **触发条件**: 权限配置格式不正确
- **解决方案**: 检查权限配置格式
- **示例**:
```json
{
  "success": false,
  "code": 2003,
  "message": "权限配置错误",
  "data": {
    "config_error": "权限类型不支持"
  }
}
```

### 3xxx 第三方集成错误

#### 3001 第三方认证失败
- **触发条件**: 钉钉、企微等登录授权失败
- **解决方案**: 
  - 检查第三方应用配置
  - 确认用户在组织内
  - 重新扫码登录
- **示例**:
```json
{
  "success": false,
  "code": 3001,
  "message": "第三方认证失败",
  "data": {
    "provider": "dingtalk",
    "error": "用户不在组织内"
  }
}
```

#### 3002 第三方配置错误
- **触发条件**: 第三方应用配置不正确
- **解决方案**: 检查app_id、secret等配置参数
- **示例**:
```json
{
  "success": false,
  "code": 3002,
  "message": "第三方配置错误",
  "data": {
    "provider": "dingtalk",
    "config_error": "app_secret无效"
  }
}
```

#### 3003 第三方服务不可用
- **触发条件**: 第三方服务临时不可用
- **解决方案**: 稍后重试或使用其他登录方式
- **示例**:
```json
{
  "success": false,
  "code": 3003,
  "message": "第三方服务不可用",
  "data": {
    "provider": "dingtalk",
    "retry_after": 300
  }
}
```

## 🔧 错误处理最佳实践

### 客户端错误处理
```javascript
async function handleAPIError(response) {
  const data = await response.json();
  
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
      reportError(data);
      break;
      
    default:
      showError(data.message);
  }
}
```

### 服务端错误记录
```python
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

def handle_business_error(error_code, message, **kwargs):
    """处理业务错误"""
    logger.error(
        f"业务错误 [{error_code}]: {message}",
        extra={
            'error_code': error_code,
            'error_data': kwargs,
            'user_id': kwargs.get('user_id'),
            'request_id': kwargs.get('request_id')
        }
    )
    
    return ApiResponse.business_error(
        message=message,
        code=error_code,
        data=kwargs
    )
```

### 错误监控和告警
```python
# 错误统计
ERROR_THRESHOLDS = {
    401: 100,  # 认证错误阈值
    403: 50,   # 权限错误阈值
    500: 10,   # 服务器错误阈值
}

def monitor_error_rate(error_code, count):
    """监控错误率"""
    threshold = ERROR_THRESHOLDS.get(error_code, 0)
    if count > threshold:
        send_alert(f"错误码 {error_code} 超过阈值: {count}/{threshold}")
```

## 📊 错误码统计

### 常见错误排行
1. **401 未授权** - 30%
2. **422 数据验证失败** - 25%
3. **403 权限不足** - 20%
4. **404 资源不存在** - 15%
5. **500 服务器错误** - 10%

### 错误趋势分析
- **认证错误**: 主要集中在Token过期和格式错误
- **权限错误**: 新用户权限配置不当
- **验证错误**: 前端数据校验不充分
- **服务器错误**: 数据库连接和第三方服务调用

## 🔗 相关文档

- [常见问题](common-issues.md) - 问题解决方案
- [调试指南](debugging.md) - 系统调试方法
- [API参考](../api-reference/responses.md) - 响应格式说明