# 模板目录结构

```
templates/
├── auth/           # 认证相关页面
│   ├── login.html     # 登录页面
│   ├── register.html  # 注册页面（待添加）
│   └── reset.html     # 密码重置页面（待添加）
├── admin/          # 管理后台模板
│   ├── base.html      # 后台基础模板（待添加）
│   └── dashboard.html # 仪表板页面（待添加）
├── users/          # 用户相关页面
│   ├── profile.html   # 用户资料页面（待添加）
│   └── settings.html  # 用户设置页面（待添加）
├── common/         # 通用组件
│   ├── base.html      # 基础模板（待添加）
│   ├── header.html    # 页头组件（待添加）
│   └── footer.html    # 页脚组件（待添加）
├── errors/         # 错误页面
│   ├── 404.html       # 404页面（待添加）
│   ├── 500.html       # 500页面（待添加）
│   └── 403.html       # 403页面（待添加）
└── README.md       # 本说明文件
```

## 命名规范

- 使用小写字母和下划线
- 文件名要有描述性
- 按功能模块分类组织
- 通用组件放在common目录
