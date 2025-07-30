# 第三方登录集成教程

## 📋 概述

本教程详细介绍如何在 Rookie 项目中集成第三方登录，包括钉钉、企业微信、飞书等平台的完整配置流程。

## 🎯 学习目标

- 了解第三方登录的工作原理
- 掌握各平台应用创建和配置方法
- 学会在系统中配置第三方登录
- 实现用户扫码登录功能

## 🔧 前置准备

### 环境要求
- Rookie 项目已正常运行
- 具有管理员权限
- 可访问第三方平台开发者后台

### 必要信息
- 企业/组织的第三方平台账号
- 应用开发权限
- 公网可访问的域名 (如: https://your-domain.com)
- SSL证书 (推荐使用HTTPS)

## 📱 钉钉登录集成

### 1. 创建钉钉应用

#### 访问钉钉开放平台
1. 登录 [钉钉开放平台](https://open.dingtalk.com/)
2. 进入 `应用开发 > 企业内部应用`
3. 点击 `创建应用`

#### 应用基本信息
```
应用名称: Rookie管理系统
应用描述: 企业级应用管理平台
应用图标: 上传应用Logo
```

#### 配置应用权限
在 `权限管理` 中申请以下权限：
- `通讯录个人信息读权限`
- `成员信息读权限`
- `通讯录部门信息读权限`

### 2. 获取应用凭证

#### 钉钉凭证说明
钉钉应用有四个凭证参数：

| 钉钉凭证 | 项目配置字段 | 说明 |
|---------|------------|------|
| **App ID** | `app_id` | 新版应用标识符 |
| **Client ID** | `client_id` | 原 AppKey/SuiteKey，用于OAuth授权 |
| **Client Secret** | `client_secret` | 原 AppSecret/SuiteSecret，用于OAuth授权 |
| **AgentId** | `agent_id` | 企业内部应用ID（可选） |

#### 记录关键信息
```
App ID: dingoa123456789
Client ID: dingoa987654321  # 原 AppKey
Client Secret: your_dingtalk_client_secret  # 原 AppSecret
AgentId: 1000001  # 企业内部应用ID（可选）
```

#### 配置服务器出口IP
在 `安全设置` 中添加服务器IP地址

### 3. 配置登录回调

#### 设置回调地址
```
登录回调地址: https://your-domain.com/api/users/third_party_callback/
```

#### 配置可信域名
```
可信域名: your-domain.com
```

**注意**: 回调地址必须是公网可访问的地址，第三方平台需要能够访问到您的服务器。

### 4. 系统中配置钉钉登录

#### 访问管理后台
```bash
# 访问配置页面
http://127.0.0.1:8000/admin/users/thirdpartyauthconfig/
```

#### 添加钉钉配置
```json
{
  "name": "dingtalk",
  "display_name": "钉钉登录",
  "is_enabled": true,
  "config": {
    "app_id": "dingoa123456789",
    "client_id": "dingoa987654321",
    "client_secret": "your_dingtalk_client_secret",
    "agent_id": "1000001",
    "corp_id": "ding123456789abcdef",
    "redirect_uri": "https://your-domain.com/api/users/third_party_callback/"
  }
}
```

**参数说明**:
- `app_id`: 新版App ID
- `client_id`: 原AppKey，用于OAuth授权
- `client_secret`: 原AppSecret，用于OAuth授权
- `agent_id`: 企业内部应用ID（可选）
- `corp_id`: 企业ID
- `redirect_uri`: 回调地址

### 5. 测试钉钉登录

#### 获取登录二维码
```bash
curl http://127.0.0.1:8000/api/users/third_party_providers/
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

#### 扫码登录流程
1. 访问登录页面: http://127.0.0.1:8000/login/
2. 切换到 `扫码登录` 标签
3. 选择 `钉钉登录`
4. 使用钉钉APP扫码
5. 确认登录授权
6. 自动跳转到管理后台

## 🏢 企业微信登录集成

### 1. 创建企业微信应用

#### 访问企业微信管理后台
1. 登录 [企业微信管理后台](https://work.weixin.qq.com/)
2. 进入 `应用管理 > 自建应用`
3. 点击 `创建应用`

#### 应用基本信息
```
应用名称: Rookie管理系统
应用介绍: 企业级应用管理平台
应用Logo: 上传应用图标
可见范围: 选择相关部门或人员
```

### 2. 获取应用信息

#### 记录应用凭证
```
企业ID (CorpId): ww123456789abcdef
应用ID (AgentId): 1000001
应用Secret: your_wechat_work_secret
```

### 3. 配置网页授权

#### 设置可信域名
在 `网页授权及JS-SDK` 中设置：
```
可信域名: your-domain.com
```

#### 配置授权回调域
```
授权回调域: your-domain.com
```

### 4. 系统中配置企业微信

#### 添加企业微信配置
```json
{
  "name": "wechat_work",
  "display_name": "企业微信登录",
  "is_enabled": true,
  "config": {
    "corp_id": "ww123456789abcdef",
    "agent_id": "1000001",
    "secret": "your_wechat_work_secret",
    "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/"
  }
}
```

### 5. 测试企业微信登录

#### 登录流程
1. 访问登录页面
2. 选择 `企业微信登录`
3. 使用企业微信APP扫码
4. 确认登录
5. 自动创建用户并登录

## 🐦 飞书登录集成

### 1. 创建飞书应用

#### 访问飞书开放平台
1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 进入 `开发者后台 > 应用管理`
3. 点击 `创建企业自建应用`

#### 应用基本信息
```
应用名称: Rookie管理系统
应用描述: 企业级应用管理平台
应用图标: 上传Logo
```

### 2. 配置应用权限

#### 申请权限范围
在 `权限管理` 中申请：
- `获取用户基本信息`
- `获取用户邮箱`
- `获取用户手机号`
- `获取用户部门信息`

### 3. 获取应用凭证

#### 记录关键信息
```
App ID: cli_a123456789abcdef
App Secret: your_feishu_app_secret
```

### 4. 配置重定向URL

#### 设置回调地址
```
重定向URL: http://127.0.0.1:8000/api/users/third_party_callback/
```

### 5. 系统中配置飞书

#### 添加飞书配置
```json
{
  "name": "feishu",
  "display_name": "飞书登录",
  "is_enabled": true,
  "config": {
    "app_id": "cli_a123456789abcdef",
    "app_secret": "your_feishu_app_secret",
    "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/"
  }
}
```

## 🔧 高级配置

### 用户信息同步

#### 当前支持的同步方式

**手动同步**: 目前项目支持手动触发用户同步

**自动同步**: 暂未实现，可作为后续功能扩展

#### 同步字段说明
第三方登录时会自动同步以下用户信息：
- `username` - 用户名/昵称
- `email` - 邮箱地址
- `phone` - 手机号码
- `department` - 部门信息
- `job_title` - 职位信息
- `employee_id` - 员工编号
- `avatar` - 头像地址

#### 手动同步用户

**通过API同步**:
```bash
curl -X POST http://127.0.0.1:8000/api/users/sync_users/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{"provider": "dingtalk"}'
```

**响应示例**:
```json
{
  "success": true,
  "code": 200,
  "message": "同步完成，共同步 15 个用户",
  "data": {
    "count": 15
  }
}
```

**注意**: 此功能需要管理员权限，且第三方平台需支持用户列表获取API

### 多平台登录

#### 同时启用多个平台
```json
[
  {
    "name": "dingtalk",
    "display_name": "钉钉登录",
    "is_enabled": true
  },
  {
    "name": "wechat_work",
    "display_name": "企业微信登录",
    "is_enabled": true
  },
  {
    "name": "feishu",
    "display_name": "飞书登录",
    "is_enabled": true
  }
]
```

#### 登录页面效果
用户可以选择任意一种方式登录：
- 账号密码登录
- 钉钉扫码登录
- 企业微信扫码登录
- 飞书扫码登录

## 🛠️ 自定义插件开发

### 创建新的登录插件

#### 1. 创建插件文件
```python
# plugins/github.py
from .base import BaseAuthPlugin
import requests

class GitHubAuthPlugin(BaseAuthPlugin):
    @property
    def name(self) -> str:
        return 'github'

    @property
    def display_name(self) -> str:
        return 'GitHub登录'

    def get_auth_url(self) -> str:
        """生成GitHub OAuth授权URL"""
        client_id = self.config.get('client_id')
        redirect_uri = self.config.get('redirect_uri')

        return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=user:email"

    def get_user_info(self, code: str) -> dict:
        """获取GitHub用户信息"""
        # 1. 获取access_token
        token_data = self._get_access_token(code)
        access_token = token_data.get('access_token')

        # 2. 获取用户信息
        user_info = self._get_user_profile(access_token)

        # 3. 标准化返回格式
        return {
            'source': 'github',
            'external_id': str(user_info.get('id')),
            'username': user_info.get('login'),
            'email': user_info.get('email'),
            'avatar': user_info.get('avatar_url')
        }
```

#### 2. 注册插件
```python
# plugins/manager.py
from .github import GitHubAuthPlugin

class PluginManager:
    def _load_plugins(self):
        plugin_classes = [
            DingTalkAuthPlugin,
            WeChatWorkAuthPlugin,
            FeishuAuthPlugin,
            GitHubAuthPlugin,  # 新增插件
        ]
```

#### 3. 配置新插件
```json
{
  "name": "github",
  "display_name": "GitHub登录",
  "is_enabled": true,
  "config": {
    "client_id": "your_github_client_id",
    "client_secret": "your_github_client_secret",
    "redirect_uri": "http://127.0.0.1:8000/api/users/third_party_callback/"
  }
}
```

## 🚨 常见问题

### Q: 扫码后提示"应用未授权"
**A**: 检查以下配置
```bash
# 1. 确认应用权限已申请并通过
# 2. 检查可信域名配置
# 3. 确认回调地址正确
# 4. 检查IP白名单设置
```

### Q: 用户信息获取失败
**A**: 检查权限配置
```bash
# 1. 确认已申请用户信息读取权限
# 2. 检查应用Secret是否正确
# 3. 确认用户在组织架构中
# 4. 查看详细错误日志
```

### Q: 回调地址访问失败
**A**: 检查网络配置
```bash
# 1. 确认回调地址可以被第三方平台访问
# 2. 检查防火墙设置
# 3. 确认域名解析正确
# 4. 测试网络连通性
```

### Q: 用户重复创建
**A**: 检查用户匹配逻辑
```bash
# 1. 确认external_id字段正确
# 2. 检查邮箱匹配逻辑
# 3. 查看用户创建日志
# 4. 手动清理重复用户
```

## 🛠️ 开发环境配置

### 本地开发解决方案

由于第三方平台需要访问公网地址，本地开发时可以使用以下方案：

#### 方案1: 使用ngrok内网穿透
```bash
# 安装ngrok
brew install ngrok  # macOS
# 或下载: https://ngrok.com/download

# 启动穿透
ngrok http 8000

# 获得公网地址
# https://abc123.ngrok.io -> http://localhost:8000
```

#### 方案2: 使用云服务器
```bash
# 部署到云服务器进行测试
# 配置域名和SSL证书
```

#### 方案3: 使用测试环境
```bash
# 搭建专门的测试环境
# 使用固定的测试域名
```

## 🔒 安全注意事项

### 1. 应用密钥保护
- 不要在前端代码中暴露Secret
- 定期更换应用密钥
- 使用环境变量存储敏感信息

### 2. 回调地址验证
- 使用HTTPS协议
- 验证state参数防止CSRF
- 检查来源IP地址

### 3. 用户信息保护
- 最小化权限申请
- 加密存储敏感信息
- 定期清理无效数据

## 📊 监控和统计

### 登录统计
```bash
# 查看第三方登录统计
curl -H "Authorization: Token your_token" \
     http://127.0.0.1:8000/api/users/statistics/
```

### 日志监控
```bash
# 查看第三方登录日志
tail -f logs/dev.log | grep "第三方登录"
```

## 🚀 功能扩展

### 自动同步功能开发

如果需要实现自动同步功能，可以考虑以下方案：

#### 1. 使用Celery定时任务
```python
# tasks.py
from celery import shared_task
from plugins.manager import plugin_manager

@shared_task
def sync_third_party_users():
    """Celery定时同步任务"""
    configs = ThirdPartyAuthConfig.objects.filter(is_enabled=True)
    for config in configs:
        plugin = plugin_manager.get_plugin(config.name, config.config)
        if plugin:
            count = plugin.sync_users()
            logger.info(f"同步{config.display_name}用户: {count}个")
```

#### 2. 扩展第三方配置模型
```python
# models.py
class ThirdPartyAuthConfig(models.Model):
    # ... 现有字段

    # 新增同步配置字段
    auto_sync_enabled = models.BooleanField('启用自动同步', default=False)
    sync_interval = models.IntegerField('同步间隔(秒)', default=3600)
    last_sync_time = models.DateTimeField('上次同步时间', null=True, blank=True)
```

#### 3. Admin后台配置界面
```python
# admin.py
class ThirdPartyAuthConfigAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'is_enabled', 'auto_sync_enabled', 'last_sync_time']
    fieldsets = [
        ('基本信息', {'fields': ['name', 'display_name', 'is_enabled']}),
        ('配置信息', {'fields': ['config']}),
        ('同步设置', {'fields': ['auto_sync_enabled', 'sync_interval']}),
    ]
```

## 🔗 相关文档

- [认证系统](../user-guide/authentication.md) - 认证机制详解
- [用户管理](../user-guide/admin-panel.md) - 用户管理后台
- [API参考](../api-reference/authentication.md) - 认证接口文档
- [故障排除](../troubleshooting/common-issues.md) - 常见问题解决
