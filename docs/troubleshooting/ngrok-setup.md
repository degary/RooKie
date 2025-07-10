# ngrok内网穿透配置指南

## 📋 概述

本文档介绍如何使用ngrok进行内网穿透，解决第三方登录开发时的回调地址问题。

## 🔧 安装ngrok

### macOS
```bash
# 使用Homebrew安装
brew install ngrok

# 或下载安装包
# https://ngrok.com/download
```

### Windows
```bash
# 下载并解压到任意目录
# https://ngrok.com/download

# 添加到系统PATH环境变量
```

### Linux
```bash
# 下载并安装
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin
```

## 🚀 使用ngrok

### 1. 启动Django项目
```bash
python manage.py runserver 8000
```

### 2. 启动ngrok穿透
```bash
# 穿透8000端口
ngrok http 8000

# 指定域名（需要付费账户）
ngrok http 8000 --hostname=your-custom-domain.ngrok.io
```

### 3. 获取公网地址
ngrok启动后会显示类似信息：
```
ngrok                                                          

Session Status                online                          
Account                       your-email@example.com (Plan: Free)
Version                       3.0.0                           
Region                        United States (us)              
Latency                       45ms                            
Web Interface                 http://127.0.0.1:4040          
Forwarding                    https://6cc54b1a26d0.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**公网地址**: `https://6cc54b1a26d0.ngrok-free.app`

## ⚙️ Django配置

### 1. CSRF配置
项目已在 `settings/dev.py` 中配置了ngrok支持：

```python
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000', 
    'https://*.ngrok.io',
    'https://*.ngrok-free.app',
    'https://*.ngrok.app',
]
```

### 2. 第三方登录配置
使用ngrok地址配置回调URL：

```json
{
  "name": "dingtalk",
  "display_name": "钉钉登录",
  "is_enabled": true,
  "config": {
    "app_id": "dingoa123456789",
    "client_id": "dingoa987654321", 
    "client_secret": "your_client_secret",
    "corp_id": "ding123456789abcdef",
    "redirect_uri": "https://6cc54b1a26d0.ngrok-free.app/api/users/third_party_callback/"
  }
}
```

## 🔧 常见问题

### Q: ngrok地址每次都变化
**A**: 免费版ngrok每次启动都会生成新的随机域名
```bash
# 解决方案1: 使用付费版固定域名
ngrok http 8000 --hostname=your-domain.ngrok.io

# 解决方案2: 使用配置文件
# ~/.ngrok2/ngrok.yml
authtoken: your_auth_token
tunnels:
  rookie:
    addr: 8000
    proto: http
    hostname: your-domain.ngrok.io

# 启动指定隧道
ngrok start rookie
```

### Q: 访问提示"Visit Site"页面
**A**: ngrok免费版会显示警告页面
```bash
# 点击"Visit Site"继续访问
# 或升级到付费版去除警告页面
```

### Q: CSRF验证失败
**A**: 确保Django配置了正确的可信来源
```python
# settings/dev.py
CSRF_TRUSTED_ORIGINS = [
    'https://your-ngrok-domain.ngrok-free.app',
]
```

### Q: 第三方平台无法访问回调地址
**A**: 检查ngrok状态和网络连接
```bash
# 查看ngrok状态
curl -s http://localhost:4040/api/tunnels | jq

# 测试公网访问
curl https://your-ngrok-domain.ngrok-free.app/api/users/third_party_providers/
```

## 🌐 Web界面监控

ngrok提供Web界面监控请求：

1. 访问: http://127.0.0.1:4040
2. 查看所有HTTP请求和响应
3. 重放请求进行调试

## 💡 最佳实践

### 1. 开发流程
```bash
# 1. 启动Django
python manage.py runserver 8000

# 2. 启动ngrok
ngrok http 8000

# 3. 复制公网地址
# 4. 更新第三方平台回调配置
# 5. 更新Django配置中的redirect_uri
# 6. 测试第三方登录
```

### 2. 配置管理
```bash
# 创建ngrok配置文件
mkdir -p ~/.ngrok2
cat > ~/.ngrok2/ngrok.yml << EOF
authtoken: your_auth_token
region: ap
tunnels:
  rookie-dev:
    addr: 8000
    proto: http
    bind_tls: true
EOF

# 使用配置启动
ngrok start rookie-dev
```

### 3. 团队协作
- 使用固定域名避免频繁更改配置
- 文档记录当前使用的ngrok地址
- 建立专用的测试环境

## 🔗 相关链接

- [ngrok官网](https://ngrok.com/)
- [ngrok文档](https://ngrok.com/docs)
- [第三方登录教程](../tutorials/third-party-login.md)