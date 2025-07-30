# API参考文档

## 📋 概述

本节提供 Rookie 项目的完整 API 接口文档，包括请求格式、响应结构、错误码说明等详细信息。

## 🌐 API基础信息

### 服务地址
- **开发环境**: `http://127.0.0.1:8000/api/`
- **测试环境**: `http://test.rookie.com/api/`
- **生产环境**: `https://api.rookie.com/api/`

### 通用信息
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8
- **API版本**: v1

## 📚 接口分类

### 🔐 认证相关
- [认证接口](authentication.md) - 登录、注册、Token管理、第三方登录

### 👥 用户管理
- [用户接口](users.md) - 用户信息、资料管理、权限查询

### 🔑 权限管理
- [权限接口](permissions.md) - 权限检查、模块管理、用户组操作

### 📋 响应格式
- [响应格式](responses.md) - 统一响应结构、错误码说明

## 🔐 认证方式

### Token认证 (推荐)
```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Session认证
```http
Cookie: sessionid=abc123...
```

## 📊 统一响应格式

### 成功响应
```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": {...},
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "abc12345"
}
```

### 错误响应
```json
{
  "success": false,
  "code": 400,
  "message": "请求参数错误",
  "data": {...},
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "def67890"
}
```

## 🚨 常见错误码

| 状态码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 请求成功 | - |
| 201 | 创建成功 | - |
| 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 未授权访问 | 检查Token或重新登录 |
| 403 | 权限不足 | 联系管理员分配权限 |
| 404 | 资源不存在 | 检查请求路径 |
| 422 | 数据验证失败 | 检查数据格式和必填字段 |
| 500 | 服务器内部错误 | 联系技术支持 |

## 📝 请求规范

### 请求头
```http
Content-Type: application/json
Authorization: Token your_token_here
Accept: application/json
```

### 请求体
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

## 🔧 调试工具

### cURL示例
```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Postman集合
- 导入Postman集合文件
- 配置环境变量
- 自动Token管理

## 📊 API限制

### 请求频率
- 默认: 无限制
- 可配置: 1000次/小时

### 数据大小
- 请求体: 最大10MB
- 响应数据: 分页返回

### 超时设置
- 连接超时: 30秒
- 读取超时: 60秒

## 🔗 相关资源

- [Postman集合](https://www.postman.com/rookie-api)
- [OpenAPI规范](https://swagger.io/specification/)
- [API测试工具](../tutorials/api-testing.md)

## 📞 技术支持

- 📧 邮件: api-support@rookie.com
- 💬 社区: [GitHub Issues](https://github.com/degary/RooKie/issues)
- 📖 文档: [在线文档](https://docs.rookie.com)
