# 故障排除

## 📋 概述

本节提供 Rookie 项目常见问题的解决方案和调试指南，帮助您快速定位和解决问题。

## 🔍 问题分类

### 🚀 安装和启动问题
- [常见问题](common-issues.md#安装启动问题) - 环境配置、依赖安装、服务启动
- [调试指南](debugging.md#启动调试) - 启动失败的排查方法

### 🔐 认证和权限问题
- [常见问题](common-issues.md#认证权限问题) - 登录失败、Token无效、权限不足
- [错误码说明](error-codes.md#认证错误) - 401、403等认证相关错误

### 🌐 API调用问题
- [常见问题](common-issues.md#API调用问题) - 接口调用失败、响应异常
- [错误码说明](error-codes.md#API错误) - 400、422、500等API错误

### 🔧 配置和部署问题
- [常见问题](common-issues.md#配置部署问题) - 数据库连接、环境配置、第三方集成
- [调试指南](debugging.md#部署调试) - 生产环境问题排查

## 🆘 快速解决

### 最常见问题

#### 1. 服务器启动失败
```bash
# 检查端口占用
lsof -i :8000

# 使用其他端口
python manage.py runserver 8001
```

#### 2. Token认证失败
```bash
# 检查Token格式
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# 重新获取Token
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'
```

#### 3. 权限不足
```bash
# 检查用户权限
curl -H "Authorization: Token your_token" \
     http://127.0.0.1:8000/api/users/my_modules/

# 在Admin后台分配权限
http://127.0.0.1:8000/admin/auth/group/
```

#### 4. 数据库连接失败
```bash
# 检查数据库配置
# 确认数据库服务运行状态
# 验证连接参数

# 重新迁移数据库
python manage.py migrate
```

## 🔧 调试工具

### 日志查看
```bash
# 查看应用日志
tail -f logs/dev.log

# 查看错误日志
tail -f logs/error.log

# 实时监控日志
tail -f logs/dev.log | grep ERROR
```

### 数据库检查
```bash
# 检查数据库连接
python manage.py dbshell

# 查看迁移状态
python manage.py showmigrations

# 检查数据完整性
python manage.py check
```

### API测试
```bash
# 测试API连通性
curl http://127.0.0.1:8000/api/users/third_party_providers/

# 测试认证接口
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'
```

## 📞 获取帮助

### 自助排查
1. 查看 [常见问题](common-issues.md)
2. 检查 [错误码说明](error-codes.md)
3. 参考 [调试指南](debugging.md)

### 社区支持
- 💬 [GitHub Issues](https://github.com/degary/RooKie/issues)
- 📖 [在线文档](https://docs.rookie.com)
- 💡 [讨论区](https://github.com/degary/RooKie/discussions)

### 技术支持
- 📧 邮件: support@rookie.com
- 🔧 技术支持: tech-support@rookie.com

## 📝 问题反馈

### 反馈模板
```markdown
## 问题描述
简要描述遇到的问题

## 环境信息
- 操作系统: 
- Python版本: 
- 项目版本: 
- 浏览器: 

## 复现步骤
1. 
2. 
3. 

## 预期结果
描述期望的正常行为

## 实际结果
描述实际发生的情况

## 错误信息
粘贴相关的错误日志或截图

## 其他信息
任何可能有助于解决问题的额外信息
```

## 🔗 相关文档

- [用户指南](../user-guide/README.md) - 功能使用说明
- [开发指南](../developer-guide/README.md) - 开发和部署指南
- [API参考](../api-reference/README.md) - 接口文档