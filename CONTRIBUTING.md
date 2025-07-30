# 贡献指南

## 🤝 欢迎贡献

感谢您对 Rookie 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ✨ 添加新功能

## 📋 贡献流程

### 1. 准备工作

```bash
# Fork 项目到你的 GitHub 账户
# 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/RooKie.git
cd RooKie

# 添加上游仓库
git remote add upstream https://github.com/degary/RooKie.git

# 创建开发环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

### 2. 开发流程

```bash
# 创建功能分支
git checkout -b feature/your-feature-name

# 进行开发
# ... 编写代码 ...

# 运行测试
python manage.py test

# 代码格式化
black .
isort .
flake8 .

# 提交代码
git add .
git commit -m "feat: 添加新功能描述"

# 推送到你的 Fork
git push origin feature/your-feature-name
```

### 3. 提交 Pull Request

1. 在 GitHub 上创建 Pull Request
2. 填写 PR 模板中的信息
3. 等待代码审查
4. 根据反馈修改代码
5. 合并到主分支

## 🔧 开发环境设置

### 必需工具

- Python 3.8+
- Git
- 代码编辑器 (推荐 VS Code)

### 推荐工具

- Docker (容器化开发)
- PostgreSQL (生产环境数据库)
- Redis (缓存)

### VS Code 配置

创建 `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Pre-commit 钩子

```bash
# 安装 pre-commit
pip install pre-commit

# 安装钩子
pre-commit install

# 手动运行检查
pre-commit run --all-files
```

## 📝 代码规范

### Python 代码风格

我们使用以下工具确保代码质量：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **mypy**: 类型检查

### 命名规范

```python
# 类名：大驼峰
class UserManager:
    pass

# 函数名：小写+下划线
def get_user_profile():
    pass

# 变量名：小写+下划线
user_email = "user@example.com"

# 常量：大写+下划线
MAX_LOGIN_ATTEMPTS = 5

# 私有方法：前缀下划线
def _internal_method():
    pass
```

### 文档字符串

```python
def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    用户认证函数

    Args:
        email (str): 用户邮箱
        password (str): 用户密码

    Returns:
        Optional[User]: 认证成功返回用户对象，失败返回None

    Raises:
        ValidationError: 当邮箱格式不正确时

    Example:
        >>> user = authenticate_user("admin@example.com", "password123")
        >>> if user:
        ...     print(f"登录成功: {user.email}")
    """
    pass
```

## 🧪 测试规范

### 测试结构

```
tests/
├── unit/           # 单元测试
│   ├── test_models.py
│   ├── test_views.py
│   └── test_utils.py
├── integration/    # 集成测试
│   ├── test_api.py
│   └── test_auth.py
└── fixtures/       # 测试数据
    └── test_data.json
```

### 测试示例

```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserAPITestCase(TestCase):
    def setUp(self):
        """测试前准备"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_user_login(self):
        """测试用户登录"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data['data'])

    def test_user_profile(self):
        """测试获取用户资料"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], self.user.email)
```

### 运行测试

```bash
# 运行所有测试
python manage.py test

# 运行特定测试
python manage.py test users.tests.test_models

# 生成覆盖率报告
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📚 文档规范

### 文档结构

- 使用 Markdown 格式
- 遵循统一的目录结构
- 包含代码示例和截图
- 保持文档与代码同步

### 文档模板

```markdown
# 标题

## 📋 概述

简要描述功能或模块的作用。

## 🚀 快速开始

### 安装

\`\`\`bash
pip install package-name
\`\`\`

### 基本使用

\`\`\`python
from module import function
result = function()
\`\`\`

## 📖 详细说明

### 功能特性

- 特性1
- 特性2

### 配置选项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| param1 | str | "default" | 参数说明 |

## 💡 示例

### 示例1：基本用法

\`\`\`python
# 代码示例
\`\`\`

## ❗ 注意事项

- 注意事项1
- 注意事项2

## 🔗 相关链接

- [相关文档](link)
```

## 🐛 Bug 报告

### Bug 报告模板

使用 GitHub Issues 报告 Bug 时，请包含以下信息：

```markdown
## Bug 描述
简要描述遇到的问题

## 复现步骤
1. 执行操作A
2. 执行操作B
3. 看到错误

## 预期行为
描述你期望发生的情况

## 实际行为
描述实际发生的情况

## 环境信息
- OS: [e.g. macOS 12.0]
- Python: [e.g. 3.9.0]
- Django: [e.g. 4.2.0]
- 浏览器: [e.g. Chrome 95.0]

## 错误日志
```
粘贴相关的错误日志
```

## 附加信息
其他可能有用的信息
```

## 💡 功能建议

### 功能建议模板

```markdown
## 功能描述
简要描述建议的新功能

## 使用场景
描述什么情况下需要这个功能

## 解决方案
描述你认为可行的实现方案

## 替代方案
描述其他可能的实现方式

## 附加信息
其他相关信息
```

## 🏷️ 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 类型说明

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例

```
feat(auth): 添加第三方登录支持

- 支持钉钉扫码登录
- 支持企业微信登录
- 添加用户信息同步功能

Closes #123
```

## 🔍 代码审查

### 审查清单

- [ ] 代码符合项目规范
- [ ] 包含适当的测试
- [ ] 文档已更新
- [ ] 没有明显的性能问题
- [ ] 安全性考虑充分
- [ ] 向后兼容性

### 审查流程

1. 自动化检查通过
2. 至少一个维护者审查
3. 所有讨论已解决
4. 测试覆盖率满足要求

## 📞 获取帮助

- 💬 [GitHub Discussions](https://github.com/degary/RooKie/discussions)
- 📧 邮件: dev@rookie.com
- 📖 [项目文档](docs/README.md)

## 🙏 致谢

感谢所有为 Rookie 项目做出贡献的开发者！

---

**最后更新**: 2024-01-01
