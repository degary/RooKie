# Rookie

<div align="center">

![Rookie Logo](https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg)

**一个开箱即用的 Django 企业级 Web 应用框架**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[English](README_EN.md) | 简体中文

</div>

## 📖 项目简介

Rookie 是一个专为企业级应用设计的 Django Web 应用框架，提供完整的用户管理、权限控制、第三方登录集成等功能。通过模块化设计和丰富的工具集，帮助开发者快速构建安全、可扩展的企业应用。

### 🎯 设计理念

- **开箱即用**: 提供完整的企业级功能模块
- **安全第一**: 内置多层安全防护机制
- **易于扩展**: 插件化架构，支持自定义扩展
- **开发友好**: 丰富的工具集和详细的文档

## ✨ 核心特性

### 🔐 完整认证系统
- **多种认证方式**: Token、Session、第三方OAuth
- **安全策略**: 密码策略、登录限制、会话管理
- **用户生命周期**: 注册、验证、激活、禁用

### 🔑 精细权限控制
- **模块级权限**: 基于业务模块的权限划分
- **角色管理**: 支持用户组和直接授权
- **权限继承**: 部门级权限继承机制
- **动态权限**: 运行时权限检查和管理

### 🌐 第三方登录集成
- **企业平台**: 钉钉、企业微信、飞书
- **扫码登录**: 二维码登录支持
- **用户同步**: 自动同步组织架构和用户信息
- **插件架构**: 易于扩展新的登录方式

### 📊 统一API响应
- **标准格式**: 统一的成功/错误响应结构
- **错误处理**: 全局异常处理和错误码管理
- **API文档**: 自动生成的 Swagger/OpenAPI 文档
- **版本控制**: API版本管理支持

### 🎨 现代化管理界面
- **Ant Design**: 基于 Ant Design 的美观界面
- **响应式设计**: 支持桌面和移动端
- **主题定制**: 支持暗色/亮色主题切换
- **国际化**: 多语言支持

### �️ 开发工具集
- **日志系统**: 基于 Loguru 的高性能日志
- **工具模块**: 丰富的工具函数和装饰器
- **测试支持**: 完整的测试框架和示例
- **部署方案**: Docker 容器化部署

## � 快速开始

### 环境要求

- Python 3.8+
- Django 4.2+
- PostgreSQL 12+ (生产环境推荐)

### 安装部署

```bash
# 1. 克隆项目
git clone https://github.com/degary/RooKie.git
cd RooKie

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 环境配置
cp .env.example .env
# 编辑 .env 文件，配置数据库等信息

# 5. 初始化数据库
python manage.py migrate

# 6. 创建演示数据
python examples/admin_demo.py

# 7. 启动开发服务器
python manage.py runserver
```

### 访问应用

- **管理后台**: http://127.0.0.1:8000/admin/
- **API文档**: http://127.0.0.1:8000/api/docs/
- **登录页面**: http://127.0.0.1:8000/login/

**默认管理员账户**: 
- 邮箱: `admin@example.com`
- 密码: `password123`

## 📡 API 使用示例

### 用户认证

```bash
# 用户登录
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'

# 响应示例
{
  "success": true,
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "admin@example.com",
      "username": "admin"
    },
    "token": "your-token-here"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Token 认证

```bash
# 使用Token访问受保护的API
curl -H "Authorization: Token your-token-here" \
     http://127.0.0.1:8000/api/users/profile/

# 获取用户模块权限
curl -H "Authorization: Token your-token-here" \
     http://127.0.0.1:8000/api/users/my_modules/
```

### 第三方登录

```bash
# 获取可用的第三方登录方式
curl http://127.0.0.1:8000/api/users/third_party_providers/

# 响应示例
{
  "success": true,
  "data": {
    "providers": [
      {
        "name": "dingtalk",
        "display_name": "钉钉登录",
        "corp_id": "your-corp-id",
        "client_id": "your-client-id"
      }
    ]
  }
}
```

## 🏗️ 技术架构

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Django | 4.2+ | Web框架 |
| Django REST Framework | 3.14+ | API框架 |
| PostgreSQL | 12+ | 数据库 |
| Redis | 6+ | 缓存 |
| Loguru | 0.7+ | 日志系统 |
| Gunicorn | 21+ | WSGI服务器 |

### 项目结构

```
RooKie/
├── Rookie/                 # Django项目配置
│   ├── settings/          # 分环境配置
│   │   ├── base.py       # 基础配置
│   │   ├── dev.py        # 开发环境
│   │   └── prod.py       # 生产环境
│   ├── urls.py           # 路由配置
│   └── wsgi.py           # WSGI入口
├── users/                 # 用户管理模块
│   ├── models.py         # 用户模型
│   ├── views.py          # API视图
│   ├── serializers.py    # 序列化器
│   └── admin.py          # 后台管理
├── plugins/               # 第三方登录插件
│   ├── base.py           # 插件基类
│   ├── dingtalk/         # 钉钉登录
│   └── wechat_work.py    # 企业微信
├── utils/                 # 工具模块
│   ├── response/         # 响应包装器
│   ├── auth/             # 权限工具
│   ├── logger.py         # 日志工具
│   └── README.md         # 工具文档
├── templates/             # 模板文件
├── static/                # 静态文件
├── docs/                  # 项目文档
├── examples/              # 示例代码
├── tests/                 # 测试代码
├── docker-compose.yml     # Docker编排
├── Dockerfile            # Docker镜像
├── requirements.txt      # Python依赖
└── manage.py             # Django管理脚本
```

## 📚 详细文档

### 📖 用户指南
- [📦 安装部署](docs/getting-started/installation.md) - 详细的安装和配置指南
- [⚡ 快速入门](docs/getting-started/quick-start.md) - 5分钟快速体验
- [🔐 认证系统](docs/user-guide/authentication.md) - 登录认证和Token使用
- [🔑 权限管理](docs/user-guide/permissions.md) - 权限配置和管理
- [📊 管理后台](docs/user-guide/admin-panel.md) - Admin后台使用指南

### 🛠️ 开发指南
- [🏗️ 系统架构](docs/developer-guide/architecture.md) - 项目架构和设计理念
- [📝 编码规范](docs/developer-guide/coding-standards.md) - 代码规范和最佳实践
- [🧪 测试指南](docs/developer-guide/testing.md) - 测试方法和规范
- [🚀 部署指南](docs/developer-guide/deployment.md) - 生产环境部署

### 📡 API参考
- [🔐 认证接口](docs/api-reference/authentication.md) - 登录、注册、Token管理
- [👥 用户接口](docs/api-reference/users.md) - 用户管理相关接口
- [🔑 权限接口](docs/api-reference/permissions.md) - 权限查询和管理
- [📋 响应格式](docs/api-reference/responses.md) - 统一响应格式说明

### 🎓 教程示例
- [🔑 Token认证教程](docs/tutorials/token-auth-tutorial.md) - Token认证完整实践
- [🔐 权限配置教程](docs/tutorials/permission-tutorial.md) - 权限系统配置实践
- [🌐 第三方登录教程](docs/tutorials/third-party-login.md) - 第三方登录集成

## 🐳 Docker 部署

### 开发环境

```bash
# 启动开发环境
docker-compose up -d

# 查看日志
docker-compose logs -f web

# 进入容器
docker-compose exec web bash
```

### 生产环境

```bash
# 设置环境变量
export SECRET_KEY="your-secret-key"
export DB_PASSWORD="your-db-password"

# 启动生产环境
docker-compose -f docker-compose.yml up -d

# 初始化数据库
docker-compose exec web python manage.py migrate
docker-compose exec web python examples/admin_demo.py
```

## 🔧 配置说明

### 环境变量

```bash
# .env 文件示例
DJANGO_ENV=dev                    # 环境: dev/prod
SECRET_KEY=your-secret-key        # Django密钥
DEBUG=True                        # 调试模式

# 数据库配置
DB_HOST=localhost
DB_NAME=rookie
DB_USER=rookie
DB_PASSWORD=password

# 第三方登录配置
DINGTALK_CORP_ID=your-corp-id
DINGTALK_CLIENT_ID=your-client-id
DINGTALK_CLIENT_SECRET=your-secret
```

### 第三方登录配置

在管理后台的"第三方认证配置"中添加：

```json
{
  "corp_id": "your-dingtalk-corp-id",
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "redirect_uri": "http://your-domain.com/api/users/third_party_callback/"
}
```

## 🧪 测试

```bash
# 运行所有测试
python manage.py test

# 运行特定模块测试
python manage.py test users

# 生成覆盖率报告
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🤝 贡献指南

我们欢迎各种形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详细信息。

### 贡献流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 开发规范

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码规范
- 使用 [Conventional Commits](https://www.conventionalcommits.org/) 提交规范
- 编写单元测试和文档
- 确保代码覆盖率 > 80%

## 📈 路线图

### v1.1.0 (计划中)
- [ ] 移动端适配优化
- [ ] 更多第三方登录支持 (GitHub, Google)
- [ ] 权限系统可视化管理
- [ ] 操作审计日志

### v1.2.0 (计划中)
- [ ] 微服务架构支持
- [ ] GraphQL API
- [ ] 实时通知系统
- [ ] 数据分析仪表板

查看完整路线图: [TODO.md](TODO.md)

## 🆘 故障排除

### 常见问题

**Q: 启动时出现数据库连接错误？**
A: 检查数据库配置和连接信息，确保数据库服务正在运行。

**Q: 第三方登录配置后无法使用？**
A: 检查回调URL配置，确保域名和端口正确。

**Q: Token认证失败？**
A: 确认Token格式正确，应为 `Token your-token-here`。

更多问题解决方案: [故障排除指南](docs/troubleshooting/common-issues.md)

## 📞 获取帮助

- 📧 **邮件支持**: support@rookie.com
- 💬 **社区讨论**: [GitHub Discussions](https://github.com/degary/RooKie/discussions)
- 🐛 **问题报告**: [GitHub Issues](https://github.com/degary/RooKie/issues)
- 📖 **在线文档**: [项目文档](https://rookie-docs.com)

## 🙏 致谢

感谢所有为 Rookie 项目做出贡献的开发者和用户！

特别感谢以下开源项目：
- [Django](https://www.djangoproject.com/) - Web框架
- [Django REST Framework](https://www.django-rest-framework.org/) - API框架
- [SimpleUI](https://github.com/newpanjing/simpleui) - 管理界面
- [Loguru](https://github.com/Delgan/loguru) - 日志系统

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

---

<div align="center">

**如果这个项目对你有帮助，请给我们一个 ⭐️**

Made with ❤️ by [degary](https://github.com/degary)

</div>
