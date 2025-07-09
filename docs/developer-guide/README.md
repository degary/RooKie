# 开发指南

## 📋 概述

本节为 Rookie 项目的开发者和贡献者提供详细的开发指南，包括系统架构、编码规范、测试方法和部署流程。

## 🎯 适用人群

- **项目开发者**: 参与项目开发的工程师
- **代码贡献者**: 提交PR的开源贡献者
- **系统架构师**: 了解系统设计的技术人员
- **运维工程师**: 负责部署和维护的运维人员

## 📚 指南目录

### 🏗️ 架构设计
- [系统架构](architecture.md) - 项目整体架构和设计理念
- [模块设计](modules.md) - 各功能模块的详细设计

### 📝 开发规范
- [编码规范](coding-standards.md) - 代码风格和最佳实践
- [API设计规范](api-design.md) - RESTful API设计标准

### 🧪 测试指南
- [测试指南](testing.md) - 单元测试、集成测试方法
- [测试覆盖率](test-coverage.md) - 测试覆盖率要求和工具

### 🚀 部署运维
- [部署指南](deployment.md) - 开发、测试、生产环境部署
- [监控运维](monitoring.md) - 系统监控和日志管理

## 🛠️ 开发环境

### 技术栈
- **后端框架**: Django 4.2+
- **API框架**: Django REST Framework
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **认证**: Token + Session
- **日志**: Loguru
- **管理界面**: SimpleUI

### 开发工具
- **代码编辑器**: VS Code, PyCharm
- **版本控制**: Git
- **API测试**: Postman, HTTPie
- **数据库工具**: DBeaver, pgAdmin

## 🚀 快速开始

### 1. 环境搭建
```bash
# 克隆项目
git clone https://github.com/degary/RooKie.git
cd RooKie

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 开发配置
```bash
# 设置开发环境
export DJANGO_ENV=dev

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

### 3. 代码结构
```
Rookie/
├── Rookie/                 # 项目配置
│   ├── settings/          # 分环境配置
│   │   ├── base.py        # 基础配置
│   │   ├── dev.py         # 开发环境
│   │   ├── acc.py         # 测试环境
│   │   └── prod.py        # 生产环境
│   ├── urls.py            # 主路由配置
│   └── wsgi.py            # WSGI配置
├── users/                 # 用户模块
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图逻辑
│   ├── serializers.py     # API序列化器
│   ├── admin.py           # Admin配置
│   ├── urls.py            # 路由配置
│   └── tests.py           # 测试用例
├── utils/                 # 工具模块
│   ├── response/          # 响应包装器
│   ├── auth/              # 权限工具
│   └── logger.py          # 日志工具
├── plugins/               # 第三方登录插件
├── templates/             # 模板文件
├── static/                # 静态文件
├── docs/                  # 项目文档
└── examples/              # 示例脚本
```

## 🔧 开发流程

### 1. 功能开发流程
```
需求分析 → 设计方案 → 编码实现 → 单元测试 → 集成测试 → 代码审查 → 合并主分支
```

### 2. Git工作流
```bash
# 创建功能分支
git checkout -b feature/new-feature

# 开发和提交
git add .
git commit -m "feat: 添加新功能"

# 推送分支
git push origin feature/new-feature

# 创建Pull Request
# 代码审查通过后合并
```

### 3. 代码审查要点
- 代码风格符合规范
- 功能实现正确
- 测试覆盖充分
- 文档更新完整
- 性能和安全考虑

## 📊 质量保证

### 代码质量
- **代码风格**: 遵循PEP 8规范
- **类型提示**: 使用Python类型注解
- **文档字符串**: 完整的函数和类文档
- **错误处理**: 适当的异常处理

### 测试要求
- **单元测试**: 覆盖率 > 80%
- **集成测试**: 关键业务流程测试
- **API测试**: 所有接口的功能测试
- **性能测试**: 关键接口的性能测试

## 🔗 相关资源

### 官方文档
- [Django文档](https://docs.djangoproject.com/)
- [DRF文档](https://www.django-rest-framework.org/)
- [Python文档](https://docs.python.org/)

### 开发工具
- [VS Code插件推荐](https://code.visualstudio.com/docs/python/python-tutorial)
- [PyCharm配置](https://www.jetbrains.com/pycharm/)
- [Git最佳实践](https://git-scm.com/book)

## 🤝 贡献指南

### 如何贡献
1. Fork项目仓库
2. 创建功能分支
3. 实现功能并添加测试
4. 更新相关文档
5. 提交Pull Request

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能开发
- 📝 文档改进
- 🎨 代码重构
- ⚡ 性能优化

## 📞 技术支持

- 💬 [GitHub Issues](https://github.com/degary/RooKie/issues)
- 📧 开发者邮件: dev@rookie.com
- 💡 [讨论区](https://github.com/degary/RooKie/discussions)